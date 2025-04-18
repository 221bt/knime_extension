import json
from FCL.fcl_generator import generate_fcl

import logging
import knime.extension as knext
LOGGER = logging.getLogger(__name__)

main_category = knext.category(
    path="/community",
    level_id="221bt",
    name="221bt",
    description="Knime Extensions by 221bt",
    icon="icons/221bt.jpg",
)

converter_category = knext.category(
    path=main_category,
    level_id="converter",
    name="Converter",
    description="Data Converter for EPCIS Document",
    icon="icons/converter_category.png",
)

@knext.node(name="FCL Converter", node_type=knext.NodeType.MANIPULATOR, icon_path="icons/fcl_converter.png", category=converter_category)
@knext.input_table(name="Input Data", description="Input EPCIS")
@knext.output_table(name="Output Data", description="Generated FCL data")
class ConverterNode:
    tracking_param = knext.StringParameter("Tracking", "Tracking index in EPCIS Document", 'example:prevID')

    def configure(self, configure_context, input_schema):
        ktype = knext.string()
        return input_schema.append(knext.Column(ktype, "FCL result"))

    def execute(self, exec_context, input_table):
        df = input_table.to_pandas()
        data = df['result'][0]
        if isinstance(data, dict):
            epcis_data = data
        else:
            epcis_data = json.loads(data)
        fcl_data = generate_fcl(epcis_data, tracking_extension_name=self.tracking_param)
        df['FCL result'] = json.dumps(fcl_data, indent=4)
        return knext.Table.from_pandas(df)