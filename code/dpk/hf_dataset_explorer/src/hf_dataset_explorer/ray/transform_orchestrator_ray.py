from logging import Logger

from data_processing.data_access import DataAccessFactory
from data_processing.runtime.ray import (
    RayTransformExecutionConfiguration,
    RayTransformOrchestrator,
    RayTransformRuntimeConfiguration,
)


class RayDataSetsTransformOrchestrator(RayTransformOrchestrator):
    """
    Class implementing transform orchestration for Python. This version
    overwrites get_files_to_process method to use list_datasets method from
    HfApi and get files to process method
    """

    def __init__(
        self,
        execution_params: RayTransformExecutionConfiguration,
        data_access_factory: list[DataAccessFactory],
        runtime_config: RayTransformRuntimeConfiguration,
        logger: Logger,
    ):
        super().__init__(
            execution_params=execution_params,
            runtime_config=runtime_config,
            data_access_factory=data_access_factory,
            logger=logger,
        )
        self.dataset_list = None
        self.processed = 0

    def get_files_to_process(self) -> int:
        self.print_interval = 100
        try:
            self.dataset_list = iter(self.data_access.get_datasets_list())
        except Exception as e:
            self.logger.error(f"failed to get the list of data sets {e}")
            return 0
        return 1

    def next_file(self) -> str:
        # check if we are done based on amount of max_files
        if self.processed >= self.data_access.m_files > 0:
            return None
        try:
            self.processed += 1
            ds_info = next(self.dataset_list)
            return f"datasets/{ds_info.id}/README.md"
        except StopIteration:
            # we are done
            return None
