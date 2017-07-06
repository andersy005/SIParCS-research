import numpy as np
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint


class FeaturesGenerator:
    """
    Generator for feature vectors for prediction algorithms.
    """
    @staticmethod
    def generateContinuousData(sc, numExamples, numFeatures, numPartitions, seed):
        def mapPart(idx, part):
            rng = np.random.RandomState(hash(str(seed ^ idx)) & 0xffffffff)
            for i in part:
                yield Vectors.dense(rng.rand(numFeatures))

        return sc.parallelize(xrange(numExamples), numPartitions).mapPartitionsWithIndex(mapPart)


class LabeledDataGenerator:
    """
    Data generator for prediction problems
    """

    @staticmethod
    def generateGLMData(sc, numExamples, numFeatures, numPartitions, seed, labelType):
        """

        :param sc:
        :param numExamples:
        :param numFeatures:
        :param numPartitions:
        :param seed:
        :param labelType:  0 = unbounded real-valued labels.  2 = binary 0/1 labels
        :return: RDD[LabeledPoint]
        """
        assert labelType == 0 or labelType == 2, \
             "LabeledDataGenerator.generateGLMData given invalid labelType: %r" % labelType

        rng = np.random.RandomState(hash(str(seed ^ -1)) & 0xffffffff)
        weights = rng.rand(numFeatures)
        featuresRDD = FeaturesGenerator.generateContinuousData(sc, numExamples, numFeatures, numPartitions, seed)

        def makeLP(features):
            label = features.dot(weights)
            if labelType == 2:
                label = 1 if label > 0.0 else 0
            return LabeledPoint(label, features)
        return featuresRDD.map(makeLP)

