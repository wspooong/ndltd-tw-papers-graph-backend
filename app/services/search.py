import os
import warnings
from datetime import datetime
from typing import Dict, List, Tuple, Union

from dotenv import load_dotenv
from opensearchpy import OpenSearch
from urllib3.exceptions import SecurityWarning

from app.services.classes import Document, Edge, Node, UIDwithEmbedding, UIDwithScore
from app.services.constants import _INDEX

warnings.simplefilter("ignore", SecurityWarning)

load_dotenv()

OS_API_URL = os.getenv("OS_API_URL")
OS_API_ID = os.getenv("OS_API_USER")
OS_API_KEY = os.getenv("OS_API_PWD")

class Search:
    """
    Class for performing search operations using Opensearch.
    """

    def __init__(self) -> None:
            """
            Initializes an instance of MyClass.

            This method connects to Opensearch and initializes the `opensearch` attribute.
            If the `OS_API_URL` contains "localhost", it establishes a connection using the specified URL,
            authentication credentials, and compression settings. Otherwise, it establishes a connection
            using the specified URL and authentication credentials.

            Args:
                None

            Returns:
                None
            """
            print(f"{datetime.now()} Connecting to Opensearch...")

            if "localhost" in OS_API_URL:
                print(f"{datetime.now()} Using localhost connection...")
                self.opensearch = OpenSearch(
                    hosts=OS_API_URL,
                    http_auth=(OS_API_ID, OS_API_KEY),
                    http_compress=True,
                    verify_certs=False,
                    ssl_show_warn=False
                )
            else:
                self.opensearch = OpenSearch(
                    hosts=OS_API_URL,
                    http_auth=(OS_API_ID, OS_API_KEY),
                    http_compress=True
                )
            print(f"{datetime.now()} Connected to Opensearch!")

    def search_title_with_vector(
        self,
        vector: List[float],
        narrow_field: str = None,
        detailed_field: str = None,
        top_k: int = 10,
        num_candidates: int = 100,
        round_decimal: int = 3,
    ) -> List[UIDwithScore]:
        """
        Searches for documents with similar titles based on the given vector.

        Args:
            vector (List[float]): The vector representation of the query.
            narrow_field (str, optional): The narrow field to search in. Defaults to None.
            detailed_field (str, optional): The detailed field to search in. Defaults to None.
            top_k (int, optional): The number of top results to retrieve. Defaults to 10.
            num_candidates (int, optional): The number of candidates to consider during the search. Defaults to 100.
            round_decimal (int, optional): The number of decimal places to round the scores. Defaults to 3.

        Returns:
            List[UIDwithScore]: The list of documents with their scores.
        """
        if round_decimal < 1 or round_decimal > 7:
            raise ValueError("round_decimal must be between 1 and 7")

        match_list = []
        query = {}

        query["size"] = num_candidates

        knn_query = {
            "embedding": {
                "vector": vector,
                "k": top_k,
            }
        }

        if narrow_field:
            match_list.append({"narrow_field": narrow_field})
        if detailed_field:
            match_list.append({"detailed_field": detailed_field})

        if match_list:
            query["bool"] = {"must": [{"match": x} for x in match_list]}

        query["query"] = {"knn": knn_query}
        query["size"] = top_k

        response = self.opensearch.search(
            index=_INDEX,
            body=query if query else None,
            _source_includes=["title"],
        )

        return [
            UIDwithScore(
                uid=hit["_id"],
                title=hit["_source"]["title"],
                score=round(hit["_score"], round_decimal),
            )
            for hit in response["hits"]["hits"]
        ]

    def get_document_with_id(self, uid: str) -> Document:
        """
        Retrieves the document with the given ID.

        Args:
            uid (str): The ID of the document.

        Returns:
            Document: The document object.
        """
        response = self.opensearch.get(
            index=_INDEX,
            id=uid,
            _source_excludes=["embedding", "advisor", "title_ws", "abstract_ws"],
        )
        return Document(**response["_source"])

    def get_document_only_embedding(self, uid: str) -> UIDwithEmbedding:
        """
        Retrieves the document embedding with the given ID.

        Args:
            uid (str): The ID of the document.

        Returns:
            UIDwithEmbedding: The document ID and its embedding.
        """
        response = self.opensearch.get(
            index=_INDEX,
            id=uid,
            _source_includes=["embedding"],
        )
        return UIDwithEmbedding(uid=uid, embedding=response["_source"]["embedding"])

    def get_document_similarity_network(
        self, uid: str, layer: int = 2, n_results: int = 5
    ) -> Tuple[List[Node], List[Edge], Dict[str, Document]]:
        """
        Retrieves the document similarity network.

        Args:
            uid (str): The ID of the starting document.
            layer (int, optional): The number of layers to expand the network. Defaults to 2.
            n_results (int, optional): The number of results to retrieve for each layer. Defaults to 5.

        Returns:
            Tuple[List[Node], List[Edge], Dict[str, Document]]: The list of nodes, list of edges, and dictionary of documents.
        """
        edge_list: List[Edge] = []
        node_list: List[Node] = []
        node_list.append(Node(uid=uid, layer=0))

        for i in range(layer + 1):
            pending_nodes = [node.uid for node in node_list if node.layer == i]
            for node in pending_nodes:
                embedding: UIDwithEmbedding = self.get_document_only_embedding(uid=node)
                result: List[UIDwithScore] = self.search_title_with_vector(
                    vector=embedding.embedding,
                    top_k=n_results,
                    num_candidates=n_results,
                )

                edge_list += [
                    Edge(source=node, target=item.uid, score=item.score)
                    for item in result
                ]
                node_list += [
                    Node(uid=item.uid, layer=i + 1)
                    for item in result
                    if item.uid not in [x.uid for x in node_list]
                ]

        documents: Dict[str, Document] = {}

        for node in list(set([x.uid for x in node_list])):
            document = self.get_document_with_id(uid=node)
            documents[node] = document

        return node_list, edge_list, documents

    def get_total_documents(self) -> Dict[str, int]:
        """
        Retrieves the total number of documents in the index.

        Returns:
            int: The total number of documents.
        """
        response = self.opensearch.count(index=_INDEX)
        return {"count": response["count"]}

    def get_top_ten_field_count(
        self, year: int
    ) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        """
        Retrieves the top ten field counts for various fields in the search index.

        Returns:
            A dictionary containing the top ten field counts for each field.
            The keys of the dictionary represent the fields, and the values are lists of dictionaries.
            Each dictionary in the list represents a field value and its count.
        """
        result = dict.fromkeys(
            [
                "degree",
                "institution",
                "department",
                "detailed_field",
                "narrow_field",
                "graduated_academic_year",
                "types_of_paper",
            ]
        )

        for field in result.keys():
            response = self.opensearch.search(
                index=_INDEX,
                body={
                    "size": 0,
                    "query": {
                        "bool": {"filter": {"term": {"graduated_academic_year": year}}}
                    },
                    "aggs": {"counts": {"terms": {"field": field}}},
                },
            )
            result[field] = response["aggregations"]["counts"]["buckets"]
        return result

    def get_institution_department_stats(
        self, year: int
    ) -> List[Dict[str, Union[str, int]]]:
        """
        Retrieves the statistics of institutions and departments based on the specified year.

        Args:
            year (int): The year for which the statistics are retrieved.

        Returns:
            list: A list of dictionaries containing the institution, department, and count of documents.

        """
        response = self.opensearch.search(
            index=_INDEX,
            body={
                "size": 0,
                "query": {
                    "bool": {"filter": {"term": {"graduated_academic_year": year}}}
                },
                "aggs": {
                    "institution_counts": {
                        "terms": {"field": "institution"},
                        "aggs": {
                            "department_counts": {"terms": {"field": "department"}}
                        },
                    }
                },
            },
        )

        result = []
        for institution_bucket in response["aggregations"]["institution_counts"][
            "buckets"
        ]:
            result.append(
                {
                    "institution": institution_bucket["key"],
                    "department": "Total",
                    "count": institution_bucket["doc_count"],
                }
            )
            for department_bucket in institution_bucket["department_counts"]["buckets"]:
                result.append(
                    {
                        "institution": institution_bucket["key"],
                        "department": department_bucket["key"],
                        "count": department_bucket["doc_count"],
                    }
                )

        return result

    def search_title(self, search_string: str) -> List[Document]:
        """
        Searches for documents with a matching title.

        Args:
            search_string (str): The search string to match against document titles.

        Returns:
            List[Document]: A list of Document objects that match the search criteria.
        """
        response = self.opensearch.search(
            index=_INDEX,
            body={
                "size": 10,
                "query": {"match": {"title": search_string}},
            },
            _source_excludes=["embedding", "advisor", "title_ws", "abstract_ws"],
        )
        return [Document(**x["_source"]) for x in response["hits"]["hits"]]
