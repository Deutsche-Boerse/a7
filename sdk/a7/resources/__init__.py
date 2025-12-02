"""Resource classes for A7 API endpoints."""

from a7.resources.algo import AlgoResource
from a7.resources.auction import AuctionResource
from a7.resources.dataset import DatasetResource
from a7.resources.eobi import EOBIResource
from a7.resources.insights import InsightsResource
from a7.resources.mdp import MDPResource
from a7.resources.orderbook import OrderBookResource
from a7.resources.precalc import PrecalcResource
from a7.resources.rdi import RDIResource
from a7.resources.sd import SDResource

__all__ = [
    "AlgoResource",
    "AuctionResource",
    "DatasetResource",
    "EOBIResource",
    "InsightsResource",
    "MDPResource",
    "OrderBookResource",
    "PrecalcResource",
    "RDIResource",
    "SDResource",
]
