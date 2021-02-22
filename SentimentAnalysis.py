import os
import tensorflow as tf
import tensorflow_datasets as tfds

from Preprocessing import preprocessing ,perprocessing

filepath = "models/TEXT_ENCODER.vocab"
encoder = tfds.deprecated.text.TokenTextEncoder.load_from_file(filepath)

filepath = "models/SENTIMENT_ANALYSIS_MODEL.hdf5"
loadModel = tf.keras.models.load_model(filepath, compile=False)


#Padding the text vector
def pad_to_size(vector, size):
  zeros = [0] * (size - len(vector))
  vector.extend(zeros)
  return vector


#Predicting the sentiment of the tweet
def toPredict(review):
  encodedReview = encoder.encode(preprocessing(review))
  encodedReview = pad_to_size(encodedReview, 32)
  encodedReview = tf.cast(encodedReview, tf.float32)
  encodedReview = tf.expand_dims(encodedReview, 0)
  predictions = loadModel.predict(encodedReview)
  return predictions


#Finding sentiment of tweets
def findTweetSentiment(tweets):
    predictions = []
    try:
        for tweet in tweets:
            try:
              predictions.append(toPredict(tweet).item())

            except Exception as error:
              predictions.append(perprocessing(tweet))
        
        return predictions

    except Exception as error:
          pass


#Finding sentiment of feedback
def findFeedbackSentiment(feedback):
  try:

    score = toPredict(feedback).item()
    return score
  
  except Exception as error:
    score = perprocessing(feedback)
    return score
   
