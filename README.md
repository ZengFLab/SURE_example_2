# SURE_example_2
 
In this tutorial, we demonstrate the process of using SURE for hierarchical assembly. We continue to use the competition data provided by NeurIPS 2021 as a demonstration example. This data contains two types of batch information: one is the location where the data was generated, and the other is the sample. Considering both the location and sample batch factors, there are a total of 13 batches, some of which have too few cells. To ensure that each batch has enough cells for computation, we treat the single-cell data generated at each location as an atlas and use SURE to establish local coordinate systems. Then, we assemble the local coordinate systems to form a global coordinate system.

In this example, we provide the following code covering:
1. [Preparing the data for each location to establish local coordinate systems](./batch_prepare_mtx_files_4_SURE.py)
2. Computing the primary metacells for each local coordinate system
3. Preparing the data for establishing the global coordinate system
4. Computing the secondary metacells for the global coordinate system
5. Visualizing the results