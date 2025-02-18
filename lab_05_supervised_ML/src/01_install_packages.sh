
# Install LiabilityPredictor

# clone LiabilityPredictor project
# it says you can use assay_liability_calculator.py to make
# predictions using the model, but as of 2/2025, this script is broken
# so instead use src/predict_liability.py instead

cd src
git clone https://github.com/jimmyjbling/LiabilityPredictor.git  # already exists in src
cd LiabilityPredictor

pip install -r requirements.txt
cd ..


## h2o is an AutoML platform
pip install xgboost

pip install -f http://h2o-release.s3.amazonaws.com/h2o/latest_stable_Py.html h2o

##############
# openJDK 17 #
#############
# h2o uses java (openJDK 17), so we need to install that too

## OSX 
brew install java
# I then got an error that I was able to resolve using this
# https://stackoverflow.com/a/65601197
sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk \
     /Library/Java/JavaVirtualMachines/openjdk.jdk

## Great lakes
# The module system only has openJDK 18 (which is incompatible with h2o, so if it's loaded, unload it
module unload openjdk

# If you're using conda
conda install -c conda-forge openjdk=17
# when starting h2o.init() it should say something like
#  openjdk version "17.0.14-internal" 2025-01-21

# alternatively download and install it directly
cd ${HOME}/opt
wget https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz
tar xzvf openjdk-17.0.2_linux-x64_bin.tar.gz
rm -rf openjdk-17.0.2_linux-x64_bin.tar.gz

# set the path to find java or copy it to somewhere on the path
export PATH=${HOME}/opt/jdk-17.0.2/bin:${PATH}

# check that it's finding the right version of java
which java

#######################
##  datamol / molfeat #
#######################
pip install molfeat
pip install datamol


