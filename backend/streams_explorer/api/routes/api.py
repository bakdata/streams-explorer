from fastapi import APIRouter

from streams_explorer.api.routes import graph, metrics, node, pipelines, update

router = APIRouter()

router.include_router(update.router, prefix="/update")
router.include_router(graph.router, prefix="/graph")
router.include_router(pipelines.router, prefix="/pipelines")
router.include_router(node.router, prefix="/node")
router.include_router(metrics.router, prefix="/metrics")
