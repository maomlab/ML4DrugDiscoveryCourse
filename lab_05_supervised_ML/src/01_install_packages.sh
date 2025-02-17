
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
pip install -f http://h2o-release.s3.amazonaws.com/h2o/latest_stable_Py.html h2o

# on OSX I had to also install the java JDK
brew install java
# I then got an error that I was able to resolve using this
# https://stackoverflow.com/a/65601197
sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk \
     /Library/Java/JavaVirtualMachines/openjdk.jdk


##  datamol / molfeat
pip install molfeat
pip install datamol


