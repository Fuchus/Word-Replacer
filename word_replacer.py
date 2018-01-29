"""
A word replacer to make a dumb sentence sound verysmart.
Leonardo Martinho
2017
"""
import API
import argparse
import re
from nltk import pos_tag
import sys
from pathlib2 import Path

def sanitize_for_url(word):
	"""
	Sanitizing of a word with a regex search string - everything that is not alphanumeric, a space or a colon is
	substituted by an empty set
	Args:
		word (str): Word to sanitize
	Returns:
		str: Sanitized string
	"""
	return re.sub('[^a-zA-Z\s:]', '', word)


def remove_escapes(word):
	"""
	Removes escape backslashes that are created by various security mechanisms
	Args:
		word (str): Word to sanitize
	Returns:
		Sanitized string
	"""
	return re.sub(r'\\', '', word)


def fetch_words(url):
	"""
	Retrieving a json result set from the API module
	An API object is instantiated and a json result set is returned by calling
	the instance specific API.object.getr() function
	Args:
		url (str): URL string to instantiate the API object
	Returns:
		dict: JSON data as python dictionary
	"""
	api = API.API(url, '')
	return api.getr()

def find_max_len(text):
	"""
	A linear search of the maximum length of a particular string
	Every string in the array is looked up by its length and consequently compared
	The string with the biggest length is then returned
	Args:
		text (arr[str]): array of strings that are compared
	Returns:
		str: Word with the biggest length
	"""
	return max(text, key=len)

def find_new_word(words, word_type):
	"""
	Checks if the word type is found in the words dict. If so the word with the biggest length is chosen
	 and returned
	Args:
		words (dict): A json result set as dict
		word_type (str): The specific word type - this is actually needed as the key in the json result set dict
	Raises:
		API.requests.exceptions.HTTPError: If the key is not found in the dict (and therefore the word type is
		non-existent) - a requests.exceptions.HTTPError is raised for easier logic in the run function
	Returns:
		str: New word
	"""
	word_categories = ["sim", "syn"]
	word_list = words.get(word_type, "")
	for tag in (x for x in word_categories if x in word_list):
		word_list = word_list.get(tag)
		new_word = find_max_len(word_list)
		return new_word
	raise API.requests.exceptions.HTTPError

def run(text):
	"""
	Main function that brings everything together - the first part of the URL is used as a parameter for the instantiation
	of the API object. The string (that may be multiple sentences) is then replaced by calling other functions.
	First the string is assigned to an array of strings calling splice_words(str). Then a tuple is assigned by
	calling NLTK.pos_tag(arr[str]). A loop to the length of the text array is then started - checking if the particular word
	is a word in the standard list - check_standard(tuple[str, str]). If not, the sanitization method clean_word[str] is called
	and the URL build. The new word is then appended to the result array. If an exception was raised, all operations are skipped
	and the unchanged word is added to the result array.
	If the API comes to a halt (due to processing limits of the API key), an empty file is set to ensure stopping
	and not spamming the server for the time being.
	Args:
		baseurl (str): URL to instantiate the API object
		text (str): String to replace the words from
	Returns:
		Result string if no ValueError has been found, error message if otherwise
	"""
	baseurl = "http://words.bighugelabs.com/api/2/0311fc4c609183416bf8bae6780fb886/{}/json"
	if len(text) <= 500:
		try:
			compare = pos_tag(text.split())
			result = []
			for word, tag in compare:
				if check_standard_word(tag):
					result.append(word)
				else:
						url_word = sanitize_for_url(word)
						if not url_word: continue
						url = baseurl.format(url_word)
						try:
							new_word = find_new_word(fetch_words(url), determine_word_type(tag))
							match = re.match('[\.,\-\?\!\(\)]', word[-1])
							if match:
								result.append(new_word + match.group()) # only copies over the last character plus the new word
							else:
								result.append(new_word)
						except API.requests.exceptions.HTTPError:
							result.append(word) # old, unchanged word
							continue
			return remove_escapes(' '.join(result))
		except ValueError:
			return "Try again later. API processing limit reached."
	else: return "The text you are typing is too long to process. Sorry."

def check_standard_word(tag):
	"""
	Checks if the values from the tag are found in the exclude array
	Args:
		tag (str): Tag from nltk.pos_tag(arr[str]) function
	Returns:
		bool: If found in the array return True, False if otherwise
	"""
	exclude = ["MD", "DT", "PRP", "$PRP", "IN", "CC", "CD", "EX", "NNP", "NNPS", "POS", "PDT", "RP", "WDT", "SYM", "TO"]
	
	return tag in exclude
	
def omitted_words(words):
	"""
	Checks if new selected word is a composition of multiple words which might include
	nonsensical grammatical words which are substituted by an empty set. First regex check is to ensure the new word
	actually has spaces
	Args:
		words(str): Sequence of words with spaces
	Returns:
		str: The word either unchanged or with the substitution of the grammatical words

	"""
	if re.match('\w+\s', words):
		compare = pos_tag(splice_words(clean_word(words)))
		for word, tag in compare:
			if check_standard(tag):
				print word
				words = words.replace(word, '')
	return words
	
def determine_word_type(tag):
	"""
	Determines the word type by checking the tag returned by the nltk.pos_tag(arr[str]) function. 
	Each word in the array is marked with a special tag which can be used to find the correct type of a word.
	A selection is given in the dictionaries.
	Args:
		tag : String tag from the nltk.pos_tag(str) function that classified the particular word with a tag
	Returns:
		str: Word type as a string
	"""
	types = {
	"noun" : {"NN", "NNS", "NNPS", "FW"},
	"adjective" : {"JJ", "JJR", "JJS"},
	"verb" : {"VB", "VBD", "VBG", "VBN", "VBP", "VBZ"},
	"adverb" : {"RB", "RBR"}
	}
	for type_, set_ in types.iteritems():
		if tag in set_:
			return type_
	return "noun"

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='A small word replacer')
	parser.add_argument(metavar='text', dest='text', action='store')
	args = parser.parse_args()
	print run(args.text)
