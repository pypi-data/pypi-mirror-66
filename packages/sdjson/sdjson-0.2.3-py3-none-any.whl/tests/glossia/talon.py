from fractions import Fraction
import sdjson


# Create a custom encoder for Fraction that turns it into a string
@sdjson.encoders.register(Fraction)
def encode_str(obj):
	return str(obj)
