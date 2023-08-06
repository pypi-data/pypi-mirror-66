import joblib,os

PACKAGE_DIR = os.path.dirname(__file__)


class CommentClassifier(object):
	"""docstring for CommentClassifier"""
	def __init__(self, text=None):
		super(CommentClassifier, self).__init__()
		self.text = text
		
	def __repr__(self):
		return 'CommentClassifier(text={})'.format(self.text)


	def predict(self):
		spam_vectorizer = open(os.path.join(PACKAGE_DIR,"models/spam_vectorizer.pkl"),'rb')
		spam_cv = joblib.load(spam_vectorizer)
		spam_detector_nb_model = open(os.path.join(PACKAGE_DIR,"models/spam_detector_nb_model.pkl"),'rb')
		spam_detector_clf = joblib.load(spam_detector_nb_model)


		vetorized_text = spam_cv.transform([self.text]).toarray()
		prediction = spam_detector_clf.predict(vetorized_text)
		# return prediction
		if prediction[0] == 0:
			result = "Non-Spam"
		elif prediction[0] == 1:
			result = "Spam"

		return result

	def load(sel,model_type):
		if model_type == 'nb':
			spam_detector_nb_model = open(os.path.join(PACKAGE_DIR,"models/spam_detector_nb_model.pkl"),'rb')
			spam_detector_clf = joblib.load(spam_detector_nb_model)
		elif model_type == 'logit':
			spam_detector_nb_model = open(os.path.join(PACKAGE_DIR,"models/spam_detector_logit_model.pkl"),'rb')
			spam_detector_clf = joblib.load(spam_detector_nb_model)

		elif model_type == 'rf':
			spam_detector_nb_model = open(os.path.join(PACKAGE_DIR,"models/spam_detector_rf_model.pkl"),'rb')
			spam_detector_clf = joblib.load(spam_detector_nb_model)

		else:
			priint("Please select a model type [nb:Naive Bayes, logit:LogisticRegression, rf: RandomForest")

		return spam_detector_clf

	def classify(self,new_text):
		self.text = new_text
		result = self.predict()
		return result

	def is_spam(self,new_text):
		self.text = new_text
		result = self.predict()
		return result == 'Spam'