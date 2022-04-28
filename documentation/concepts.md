# Environments
Grizzly comes with three different environments for testing, validating, and running your Grizzly installation: **Development** (DEV), **User Acceptance Testing** (UAT), and **Production** (PROD).

The **Development (DEV) Environment** is used for your initial development of new data assets. This environment is just for you and other developers to see how new features will work and test out improvements. After you've finished development and initial testing, it's time to share these new data assets with your power users by promoting them to the User Acceptance Testing Environment (UAT).

The **User Acceptance Testing (UAT) Environment** is used by your power users to test new data assets and functionality before releasing to all of your users. The UAT environment is as similar to the production environment as can be. Since the UAT environment is isolated from in-progress development in the DEV environment, more in-depth testing is done in the UAT environment. When testing is completed, it's time to share these new data assets with your power users by promoting them to the Production Environment (PROD).

The **Production (PROD) Environment** is where users access the data assets that you've built in Grizzly. Of all environments, this is the most important. Since this environment is used by all of your users, it is the most important. Hence why testing in the DEV and UAT environments is so important.

# Cloud Projects
Each Grizzly environment corresponds to a Google Cloud Platform project. Within these projects, we store the data assets and where code is executed to generate the data assets. One project is created for each environment (DEV, UAT, and PROD).

A fourth project called "Metadata" is where we store our centralized code repository for Grizzly. It helps to orchestrate our code between the three environments and their respective cloud projects.

To tie these projects together we give each project a common stem name (ex: "finance", "marketing", etc.) to describe how they are used in your organization. We use the following naming convention:
- Production (PROD) environment: "*[stem_name]*-prod"
- User Acceptance Testing (UAT) environment: "*[stem_name]*-uat"
- Development (DEV) environment: "*[stem_name]*-dev"
- Metadata: "*[stem_name]*-metadata"

# Code Repository and Development Branches
In the code repository in the "metadata" project, we have three branches of our code -- DEV, UAT, and PROD. Each branch corresponds to one of the three Grizzly environments and represents the code and data assets deployed currently in those environments.

# Data Layers: Base, Business, and Presentation
## Base Data Layer
The **Base Data Layer** contains the raw data from around your organization that you initially import into Grizzly. Think of this as the landing area for new data into Grizzly. The data should be raw and untransformed from your source systems.

Grizzly stores all Base Data Layer Table Definitions in the /base/ folder with a subdirectory corresponding to the data source system that you are importing data from. These subdirectories and their corresponding BigQuery datasets follow the naming convention "bas_[data_source]".

See [bas_austin_crime](../grizzly_example/base/bas_austin_crime/) for an example of a Base Data Layer.

## Business Data Layer

The **Business Data Layer** is where you apply your business logic to the data you've imported in the Base Data Layer. In other data systems, this is known as the "Transform" Layer. Here you join and manipulate your base data layer so that it provides value for your business.

Grizzly stores related Business Data Layer Table Definitions in a folder based on the table's business and operation domain. For example, a domain folder would correspond to a specific knowledge area (like inventory or accounting) or a specific analysis (like store research or supply chain geography).  A domain can consist of both Business Data Layer and Presentation Data Layer datasets and tables. This helps keep related analyses grouped together in our folder structure.

BigQuery datasets within the business data layer follow the naming convention "biz_[domain_name]".

See [store_research](../grizzly_example/store_research/) for an example of a domain consisting of both the Business Data Layer and Presentation Data Layer.

## Presentation Data Layer
The **Presentation Data Layer** contains the subset of data that is presented to users through Business Intelligence tools or exported out of Grizzly to other systems. It does not contain business logic transformations. It should contain the minimal number of transformations that are required to present your data.

Just like the Business Data Layer, Grizzly stores related Presentation Data Layer Table Definitions in a folder based on the table's business and operation domain. A domain can consist of both Business Data Layer and Presentation Data Layer datasets and tables. This helps keep related analyses grouped together in our folder structure.

BigQuery datasets within the Presentation Data Layer follow the naming convention "prs_[domain_name]".

See [store_research](../grizzly_example/store_research/) for an example of a domain consisting of both the Business Data Layer and Presentation Data Layer.



