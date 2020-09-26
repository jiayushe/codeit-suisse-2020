from flask import Flask

app = Flask(__name__)

import codeitsuisse.routes.square
import codeitsuisse.routes.secret_message
import codeitsuisse.routes.salad_spree
import codeitsuisse.routes.clean_floor
import codeitsuisse.routes.contact_trace
import codeitsuisse.routes.revisit_geometry
import codeitsuisse.routes.cluster
import codeitsuisse.routes.inventory_management
import codeitsuisse.routes.social_distancing
import codeitsuisse.routes.intelligent_farming
import codeitsuisse.routes.fruit_basket
import codeitsuisse.routes.olympiad_of_babylon
import codeitsuisse.routes.optimized_portfolio
