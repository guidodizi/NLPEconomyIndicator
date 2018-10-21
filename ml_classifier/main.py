# -*- coding: utf-8 -*-
import settings
import training_preprocess
from helper_methods import *
from training_preprocess import *

# MAIN
#print_presentation()
#settings.init()

# Input sections
#option = options_input_section()
generate_training_set()
text_preproccessing()
# TODO: implementar

print_finish()
