# EPCIS Synthetic Supply Chain Data Generator KNIME Node

## Overview
This repository contains a KNIME node developed by 221BT, designed for AI/ML scientists and supply chain analysts to generate synthetic supply chain data compliant with GS1 EPCIS V2 standards. The node enables the creation of realistic, interconnected datasets that mimic food supply chain operations. These generated datasets support forward and backward tracing, network analysis, and compliance with regulatory requirements such as FDA’s FSMA Section 204. The synthetic data is ideal for developing predictive analytics, machine learning models, and anomaly detection systems to enhance traceability, optimize recall management, and ensure food safety during outbreaks.

The node’s compliance with GS1 EPCIS V2, validated using NIRA’s Oliot EPCIS X, ensures standardization, interoperability, and regulatory adherence, making it a powerful tool for both research and industry applications. Developed as part of 221BT’s mission to provide innovative solutions for supply chain visibility and efficiency, this tool unlocks a wide range of use cases, from simulating complex supply chain scenarios to training AI models for emerging challenges. Whether you’re researching supply chain resilience, testing compliance systems, or building predictive models for risk management, this node provides a robust foundation for experimentation and innovation.

Additionally, we have created a complementary KNIME node that converts EPCIS documents into the BfR FoodChain-Lab format. This allows users to leverage the advanced capabilities of FoodChain-Lab’s KNIME nodes for in-depth supply chain analysis and foodborne outbreak investigation. FoodChain-Lab is a specialized KNIME extension that facilitates trace-back and trace-forward analysis of suspicious food items along supply chains, aiding in the investigation of foodborne disease outbreaks. It supports data collection, handling, and analysis of food delivery networks, offering features such as geographical visualization, clustering, and geocoding. Users can import supply chain data, visualize delivery networks, perform tracing without visualization, and cluster stations geographically based on attributes like location and business type. For more detailed information about FoodChain-Lab, visit https://github.com/SiLeBAT/BfROpenLab.

## Changelog
### EPCIS Data Generator
#### v0.1.2:
- Move the extension to *Community Node -> 221bt* based on Knime Document recommandation.
- Fix Location Masterdata parsing error and assign role to each location based on 204 rules

### FCL Converter
#### v0.1.2:
- Move the extension to *Community Node -> 221bt* based on Knime Document recommandation.
- Support JSON input.
- Add Location Masterdata role support.

## Getting Started

1. Download and install/unzip the latest version of [KNIME](https://www.knime.com/downloads).
2. Select **Help > Install New Software** in the menu bar. And click **Add**, in the upper right corner.
3. In the Add Repository dialogue that appears, enter "EPCIS Data Generator" for the Name and the following URL for the Location: https://github.com/221bt/knime_extension/raw/release. Click **Add**.
![Add extension repo](img/Step_3.png)
4. In the Available Software dialogue, expand the "Data Generator For EPCIS 2.0 Document" entry and select the checkbox next to "Data Generator For EPCIS 2.0 Document". Click **Next**.
![Select extension](img/Step_4.png)
5. In the next window, you’ll see a list of the tools to be downloaded. Click **Finish**.
6. If a window "Trust Authorities" pops up, please tick the checkbox in the upper left corner next to "https://github.com/221bt" and click **Trust Selected**.
7. If a window pops up asking whether you trust unsigned content, please tick the checkbox in the upper left corner next to “Unsigned” and click **Trust Selected**.
8. When the installation completes, restart KNIME.
10. For FCL Converter, repeat step 2 to step 8. Replace repository name with "FCL Converter" and URL: https://github.com/221bt/knime_extension/raw/fcl_release
9. When the KNIME interface has shown up, you should be able to see an item "EPCIS Data Generator" and "FCL Converter" in the **Node Repository** view in the bottom-left corner.And you can find them under *Community Node -> 221bt*. To run the full example workflow, please install FoodChain-Lab KNIME extension from [this site](https://foodrisklabs.bfr.bund.de/installation/)
![Installation Result](img/Step_9.png)


## Example
![Exmaple 1](img/Example_1.png)

![Exmaple 2](img/Example_2.png)

![Exmaple 3](img/Example_3.png)

## Suitable Use Cases
The EPCIS-based synthetic supply chain data generated by this node can be leveraged in a variety of scenarios, making it an invaluable resource for researchers, analysts, and industry professionals. Here are some key applications:

- **Training Machine Learning Models for Traceability and Recall**: Use the synthetic data to train AI models that can quickly trace products forward (from source to consumer) and backward (from consumer to source) during recalls or outbreaks, minimizing response times and reducing risks.
- **Simulating Supply Chain Disruptions**: Generate data to model disruptions such as natural disasters, geopolitical events, or labor strikes, allowing businesses to test resilience strategies and optimize contingency plans.
- **Compliance Testing and Regulatory Preparedness**: Create datasets to simulate compliance with global standards (e.g., GS1, FDA, EU regulations) and test systems for adherence to traceability mandates, ensuring readiness for audits and inspections.
- **Network Analysis and Optimization**: Analyze the interconnectedness of supply chain networks to identify bottlenecks, vulnerabilities, or opportunities for efficiency improvements, such as reducing waste or shortening lead times.
- **Anomaly Detection for Food Safety**: Develop and test anomaly detection algorithms to identify potential contamination events, spoilage, or tampering in real-time, enhancing food safety and consumer trust.
- **Scenario Planning for Sustainability**: Generate data to evaluate the environmental impact of supply chain decisions, such as carbon footprint reduction or sustainable sourcing, supporting green initiatives and corporate sustainability goals.
- **Training and Education**: Use the node to create realistic training datasets for educational programs, workshops, or certifications in supply chain management, helping students and professionals gain hands-on experience with EPCIS standards.
- **Vendor and Partner Collaboration**: Simulate multi-tier supply chain interactions to test collaboration tools, communication protocols, and data-sharing agreements between suppliers, manufacturers, distributors, and retailers.

These use cases demonstrate the node’s versatility, enabling users to tackle both current challenges and future opportunities in supply chain management.

## Acknowledgments
We are grateful for the support and expertise provided by [Equinoxys](https://equinoxys.com/), a KNIME Award-winning partner. Their guidance and collaboration were instrumental in transforming our data-generating function into a KNIME node, ensuring it meets the needs of the AI/ML and supply chain communities. Equinoxys’ commitment to innovation and excellence in data science solutions has been a valuable asset to this project.

