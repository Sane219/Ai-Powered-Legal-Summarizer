#!/usr/bin/env python3
"""
Deployment script for the Legal Document Summarization app
Includes memory management and error recovery
"""
import os
import sys
import subprocess
import logging
import signal
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup environment variables for optimal performance"""
    # Set memory-efficient environment variables
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'  # Avoid tokenizer warnings
    os.environ['TRANSFORMERS_CACHE'] = './cache'    # Local cache directory
    os.environ['HF_HOME'] = './cache'               # Hugging Face cache
    
    # PyTorch settings for memory efficiency
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
    
    # Create cache directory
    os.makedirs('./cache', exist_ok=True)
    
    logger.info("Environment configured for optimal performance")

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        imp main()":
   ain__== "__mf __name__ 
iit()
process.wa     nate()
   ss.termioce       prn...")
 dowting info("Shutlogger.t:
        dInterruppt Keyboar exce
   s.wait()oces   prcess
      the profor# Wait 
         try:
   lit()
    eam= run_str process the app
   un   
    # R(1)
     sys.exit
     ncies")ded depenall requireall "Please instror(r.erlogge       ncies():
 ck_dependeif not che  encies
   dependheck
    # C
    t()_environmen  setupent
  up environm Set #)
    
   ."p..Apization Summart enLegal Documng "Startier.info("
    logg""tionment funceployn dai   """Mmain():
 
def )
mdss.Popen(cn subproceretur.")
    eamlit app..String "Startogger.info(
    
    l
    ]led=true"icEnab-runner.mag     "-   ",
s=falseageStattherUsrowser.ga       "--bfalse",
 bleCORS=er.enarvse   "--00",
     loadSize=2er.maxUp-serv"-      py",
  app. "run", "",reamlit-m", "stcutable, " sys.exe     = [
   cmd"
    ttings""imal septwith olit app eamthe Str  """Run mlit():
  f run_streae

dereturn Fals        }")
cy: {endeng depef"Missinogger.error(     lr as e:
   ortErroexcept Imp   rn True
  retu")
       bles are availaenciel dependnfo("Al logger.i     acy
  sp  import rs
       transformeort       imph
 orct timpor
        mlitort strea