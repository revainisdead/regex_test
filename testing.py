import re

# w: Word
# d: Digit
# s: Space

# Escape Info
# --
# outside character class: \ and ^ and $ and . and | and ? and * and + and ( and ) and [ and {
# inside character class needs escape: \ and ^ and -

def dumptext(infile):
    with open(infile, "r") as f:
        return f.read()

# findall: returns capturing groups, not matches
def finditer_print(regex, string):
    result = re.finditer(regex, string)
    print([_.group() for _ in result])


def main():
    """
    print(re.findall(r"" \
        "<([A-Za-z][A-Za-z\d]*)"   # Beginning html tag, case insensitive, 1 char, 2nd is optional
        "\b[^>]*" \                # Word bounary but not closing bracket, skips over attributes
        ">" \                      # Literal closing bracket for opening html tag
        ".*?" \                    # Characters between html tags
        "</\1>" \                  # Closing html tag, back referene to use same rules as opening
    "", "<td></td><a></a><h1></h1><div hidden=\"test\"></div>"))
    """
    print(re.findall(r"(\b\w+(?<!s)\b)", "John's"))
    print(re.findall(r"(\b\w*[^s\']\b)", "John's"))

    # Place hyphen at end of character class to negate the typical range function
    # Place caret anywhere except the beginning of the character class to specify it
    print(re.findall(r"(\b[A-Za-z0-9.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b)", "chris.ant.hall@gmail.com"))

    # Not character class
    # Match a single character that is not a digit 0-9 or a line break
    print(re.findall(r"[^0-9\n]", "testing1234\n"))

    # Create a back reference
    print(re.findall(r"([0-9])\1+", "222 837"))

    # Include these but don't include the subtracted, not supported in Python
    #print(re.findall(r"([a-z-[aeiou]])", "acbde"))
    #print(re.findall(r"[a-z&&[^aeiou]]", "acdbe"))
    print(re.findall(r"([b-df-hj-np-tv-z])", "abcde"))

    # \W opposite of \w so any character that is not [A-Za-z0-9_]
    # So it must be not a u, and basically must be a charcter or digit
    print(re.findall(r"q[^u\W]", "Iraqis a country."))
    print(re.sub("[a-z0-9]+$", "com", "www.google.x"))

    # \s is white space, followed by one character or digit
    # includes [ \t\r\n\f]: space, tab, carriage return, line feed, form feed
    print(re.findall(r"\s+[\w]", "     test"))

    # Dates! Allow separtors backslash, space, forward slash, hyphen
    print(re.findall(r"[01]\d[\\ /-][0-3]\d[\\ /-][\d]{4}", "12/01/2000"))

    # \h - horizontal line breaks: space, tab
    # \v - vertical line breaks: carriage return, line feed

    # Match quoted strings, that don't have quotes inside of them
    print(re.findall(r"\"[^\"\r\n]*\"", 'testing "string one" and "string two"'))

    # Is integer
    print(re.findall(r"^\d+$", "22asd"))
    print(re.findall(r"^\d+$", "asdb4sa"))
    print(re.findall(r"^\d+$", "1234"))

    # Match even though it has a line break
    print(re.findall(r"^\d+$", "123\n"))

    # Alternative to ^ and $: use \A and \Z
    # Match any number of digits in the beginning
    # Match a new line character right before the end
    print(re.findall(r"\A\d+\n\Z", "123\n"))

    # \b - matches {here}abcd{here} -> there's no more characters
    # \B - matches a{here}b{here}c{here}d -> there's more characters
    msg = "catmania thiscat thiscatmania"
    print(re.sub(r"\bcat", "tt", msg)) # at the beginning of each word
    print(re.sub(r"cat\b", "tt", msg)) # at the end of each word
    print(re.sub(r"\Bcat", "tt", msg)) # not in the beginning
    print(re.sub(r"cat\B", "tt", msg)) # not in the end

    # Always put word that contains other words (longer word)
    # earlier in the expression, or get optional character to work
    print(re.findall(r"Get|GetValue|Set|SetValue", "SetValue"))
    # Question mark is greedy, so it's checked first
    # Optional also means zero or one times, so if it's zero, this will also match empty.
    print(re.findall(r"Get(Value)?|Set(Value)?", "SetValue")) # INCORRECT
    print(re.findall(r"(Get(Value)?)|(Set(Value)?)", "Set SetValue Get GetValue")) # Works
    print(re.findall(r"Get(?:Value)?|Set(?:Value)?", "Set SetValue Get GetValue")) # Works

    # Incorporate Optional pieces (greedy)
    #print(re.findall("Feb(ruary)? 23(rd)?", "February 23"))
    match1 = re.match(r"Feb(ruary)? 23(rd)?", "Feb 23rd").group(0)
    match2 = re.match(r"Feb(ruary)? 23(rd)?", "February 23").group(0)

    # Find html tag
    print(re.findall(r"<[A-Za-z][A-Za-z\d]*>\w*</[A-Za-z][A-Za-z\d]*>", "<td></td><a></a><h1></h1>"))
    # Use back reference to shorten html matching
    # Matches the same, but returns the capturing new group
    print(re.findall(r"<([A-Za-z][A-Za-z\d]*)>\w*</\1>", "<td></td><a></a><h1></h1>"))

    # Use word boundary to skip over any attributes in the html tag
    VERBOSE = re.X
    MULTILINE = re.M
    print(re.findall(r"""
        (                           #
        <([A-Za-z][A-Za-z\d]*)      #
        \b[^>]*                     #
        >                           #
        \w*                         #
        </\2>                       #
        )                           #
    """, "<td></td><a></a><h1></h1><div hidden=\"test\"></div>", VERBOSE|MULTILINE))

    # The first capturing group is the same as the whole match.
    # The second capturing group is going to be the second tuple index of findall results,
    # and it specifically returns just what has matched in that group (keep in mind)
    print(re.findall("(\d+(\.\d+)?)", "3434.35353 2000.00"))

    # Dot matches everything except new line, add DOTALL to make dot match those too.
    print(re.findall(r"^(.*?)(Arguments:.*?)?(Returns:.*)?$", dumptext("text.txt"), re.DOTALL))

    # Non-capturing group: aaa is included in overall match, but not returned groups
    pattern = re.match(r"(?:aaa)(_bbb)", "aaa_bbb")
    print(pattern.group())
    print(pattern.group(1))

    # Positive lookbehind, _bbb is preceded by aaa, not aaa is NOT included in overall match.
    pattern2 = re.match(r"(?<=aaa)_bbb", "aaa_bbb")
    if pattern2:
        print(pattern2.group())
        print(pattern2.group(1))

    finditer_print(r"Feb(ruary)? 23(rd)?", "Feb 23rd February 23")

    def camel_to_snake(s):
        # The key to the first regex is that is must find the series of lower case letters
        # after the first two characters {any char}{one upper case char}
        # i.e. "PRe" in "getHTTPResponseCode"
        #       ^    any char
        #        ^   one upper case char
        #         ^  series of lower case letters (one or more)
        tmp = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", tmp)
    print(camel_to_snake("camel2_camel2_case"))
    print(camel_to_snake("getHTTPResponseCode"))
    print(camel_to_snake("HTTPResponseCodeXYZ"))

    def camel_to_snake_str(s):
        return "".join(["_" + c.lower() if c.isupper() else c for c in s])

    print(camel_to_snake_str("smallCamel"))
    print(camel_to_snake_str("veryVeryLargeCamel"))
    print(camel_to_snake_str("getHTTPResponseCode"))

    finditer_print(r"(\b\w+(?<!s)\b)", "John's test test")

    # Find any word between 6 and 12 chars that contains cat, dog, or mouse
    # Step 1: Define each requirement separately
    # Step 2: Lookahead: contains larger requirement, second part contains subset requirement
    # TIP: Don't put a space between "6," and "12"
    finditer_print(r"(?=\b\w{6,12}\b)\w*(cat|dog|mouse)\w*", "mousea aaadog cataaaa")

def last_index(s):
    return len(s) -1

if __name__ == "__main__":
    main()

