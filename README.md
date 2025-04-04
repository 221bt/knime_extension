# EPCIS Synthetic Supply Chain Data Generator KNIME Node

## Overview
This repository contains a KNIME node designed for AI/ML scientists and supply chain analysts to generate synthetic supply chain data compliant with GS1 EPCIS V2 standards. The node enables the creation of realistic, interconnected datasets mimicking food supply chain operations. Generated datasets support forward and backward tracing, network analysis, and compliance with regulatory requirements such as FDA’s FSMA Section 204. The synthetic data is ideal for developing predictive analytics, machine learning models, and anomaly detection systems to enhance traceability, optimize recall management, and ensure food safety during outbreaks.

The node was developed by 221BT as part of its mission to provide innovative solutions for supply chain visibility and efficiency. The dataset’s compliance with GS1 EPCIS V2, validated using NIRA’s Oliot EPCIS X, ensures standardization, interoperability, and regulatory adherence, making it a powerful tool for both research and industry applications.

In addition to its core functionality, this tool unlocks a wide range of use cases, from simulating complex supply chain scenarios to training AI models for emerging challenges. Whether you’re researching supply chain resilience, testing compliance systems, or building predictive models for risk management, this node provides a robust foundation for experimentation and innovation.

## Getting Started

1. Download and install/unzip the latest version of [KNIME](https://www.knime.com/downloads).
2. Select **Help > Install New Software** in the menu bar. And click **Add**, in the upper right corner.
3. In the Add Repository dialogue that appears, enter "EPCIS Data Generator" for the Name and the following URL for the Location: https://github.com/221bt/knime_extension/raw/release. Click **Add**.
![Add extension repo](img\Step_3.png)
4. In the Available Software dialogue, expand the "Data Generator For EPCIS 2.0 Document" entry and select the checkbox next to "Data Generator For EPCIS 2.0 Document". Click **Next**.
![Select extension](img\Step_4.png)
5. In the next window, you’ll see a list of the tools to be downloaded. Click **Finish**.
6. If a window "Trust Authorities" pops up, please tick the checkbox in the upper left corner next to "https://github.com/221bt" and click **Trust Selected**.
7. If a window pops up asking whether you trust unsigned content, please tick the checkbox in the upper left corner next to “Unsigned” and click **Trust Selected**.
8. When the installation completes, restart KNIME.
9. When the KNIME interface has shown up, you should be able to see an item "EPCIS Data Generator" in the **Node Repository** view in the bottom-left corner. 
![Installation Result](img\Step_9.png)

## Example
![Exmaple 1](img\Example_1.png)

![Exmaple 2](img\Example_2.png)

![Exmaple 3](img\Example_3.png)
## Acknowledgments
We are grateful for the support and expertise provided by [Equinoxys](https://equinoxys.com/), a KNIME Award-winning partner. Their guidance and collaboration were instrumental in transforming our data-generating function into a KNIME node, ensuring it meets the needs of the AI/ML and supply chain communities. Equinoxys’ commitment to innovation and excellence in data science solutions has been a valuable asset to this project.

