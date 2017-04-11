import sys

from sklearn import metrics

from FeatureExtractor import FeatureExtractor
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

class Classifier(object):
	"""docstring for Classifier"""
	def __init__(self, models="multinomial"):
		super(Classifier, self).__init__()
		if models == "multinomial":
			self.classifier = MultinomialNB()
		elif models == "svm":
			self.classifier = SVC()

	def classify(self, dataset, labels):
		self.classifier = self.classifier.fit(dataset, labels)

	def test(self, dataset):
		predictions = self.classifier.predict(dataset)
		return predictions

	def do_evaluate(self, test_set):
		predictions = self.test(test_set)
		# accuracy_score = metrics.accuracy_score()

def main(filename):
	fe = FeatureExtractor("tfidf", filename)
	fe.load_dataset()
	fe.load_labels()

	bow = fe.build_bag()
	bag = fe.build_tfidf()

	print "** Using Multinomial NB Models **"

	# TFIDF
	clf = Classifier(models="multinomial")
	clf.classify(bag, fe.raw_labels)

	preds = clf.test(bag)
	# for doc, cat in zip(fe.dataset, preds):
	# 	print "%r => %s" % (doc, cat)

	print "TFIDF accuracy score: %f" % (metrics.accuracy_score(fe.raw_labels, preds, normalize=True))
	f1_pos = metrics.f1_score(fe.raw_labels, preds, pos_label='positive')
	f1_neg = metrics.f1_score(fe.raw_labels, preds, pos_label='negative')
	print "TFIDF F1 score: %f" % (f1_pos)
	print "TFIDF F1 negative score: %f" % (f1_neg)

	print "\nAverage F-measure: %f" % ((f1_pos + f1_neg)/2) 

	# bag of words
	clf = Classifier(models="multinomial")
	clf.classify(bow, fe.raw_labels)
	preds = clf.test(bow)

	print "BOW accuracy score: %f" % (metrics.accuracy_score(fe.raw_labels, preds, normalize=True))
	print "BOW F1 score: %f" % (metrics.f1_score(fe.raw_labels, preds, pos_label='positive'))

	print "\n** Using SVM **"

	# TFIDF
	clf = Classifier(models="svm")
	clf.classify(bag, fe.raw_labels)

	preds = clf.test(bag)
	# for doc, cat in zip(fe.dataset, preds):
	# 	print "%r => %s" % (doc, cat)

	print "TFIDF accuracy score: %f" % (metrics.accuracy_score(fe.raw_labels, preds, normalize=True))

	# bag of words
	clf = Classifier(models="svm")
	clf.classify(bow, fe.raw_labels)
	preds = clf.test(bow)

	print "BOW accuracy score: %f" % (metrics.accuracy_score(fe.raw_labels, preds, normalize=True))

	X_train, X_test, y_train, y_test = train_test_split(bow, fe.raw_labels, test_size=0.4, random_state=0)
	clf = Classifier(models="svm")
	clf.classify(X_train, y_train)
	preds = clf.test(X_test)

	print "Using 60/40, BOW accuracy: %f" % (metrics.accuracy_score(y_test, preds, normalize=True))
	print "Using 60/40, BOW F1: %f" % (metrics.f1_score(y_test, preds, pos_label='positive'))

if __name__ == '__main__':
	main(sys.argv[1])