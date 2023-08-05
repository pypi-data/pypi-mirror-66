import re
import sys


# This function was separated for testing purposes. To test, main is commented out and the program begins from analyze().
def main():
    file = raw_input('Enter file name: ')
    analyze(file)


# This function takes in a string as the filename, reads through the file and separates the grid from the list of words.
def analyze(file):
    with open(file, 'r') as f:

        # This reads and removes the first line with the grid parameters. Then it saves the remaining lines of the
        # file as the variable 'text'.
        temp = f.readline()
        text = f.readlines()

    # These are lists- 'grid_lines' is the word search and 'words' is the given list of words.
    grid_lines, words = [], []

    # Each line of text is stripped to remove extra spaces, and then- based on length to separate words from the search,
    # the line is added to the appropriate list.
    for line in text:
        line = line.strip().split(" ")
        if len(line) > 1:
            grid_lines.append(line)
        else:
            words.append(line[0])

    # This dictionary stores the words and the tuples with their beginning and ending locations.
    locs = word_find(grid_lines, words)

    # The 'output' is for testing. The program writes to a file which is compared to the answer file to validate that
    # the searches are working properly.

    # **** uncomment below line for testing ****
    # output = open('output_file.txt', 'w')

    # This for-loop goes through each entry in locs and writes the word and its locations to the console.
    for entry in locs:
        temp = locs[entry]
        tuple1, tuple2 = temp[0], temp[1]

        # **** uncomment below line for testing ****
        # output.write("%s %i:%i %i:%i\n" % (entry, tuple1[0], tuple1[1], tuple2[0], tuple2[1]))

        sys.stdout.write("%s %i:%i %i:%i\n" % (entry, tuple1[0], tuple1[1], tuple2[0], tuple2[1]))
        sys.stdout.flush()

    # **** uncomment below line for testing ****
    # output.close()


# This function creates a dictionary of words and empty locations, and then passes that as well as the list of words
# and the search grid into the search functions. It then returns the dictionary.
def word_find(grid_lines, words):
    res = {}
    for word in words:
        res[word] = [(0, 0),(0, 0)]

    res = horiz_search(grid_lines, words, res)
    res = vert_search(grid_lines, words, res)
    res = left_diag(grid_lines, words, res)
    res = right_diag(grid_lines, words, res)

    return res


# This function searches for each word in the list horizontally.
def horiz_search(input, word_list, res):
    for word in word_list:
        i = 0

        # This while loop goes through each row of the search grid and joins the characters together. It then searches
        # the string for the word.
        while i < len(input):
            str = ''.join(input[i])
            ans = str.find(word)

            # If the word is found, the word and its coordinates are stored in the dictionary 'res' and the loop ends.
            if ans != -1:
                end = ans + (len(word) - 1)

                res[word] = [(i, ans), (i, end)]
                break

            # If the word is not found, the row is joined in reverse, and the search for the word is done in the
            # reversed row.
            else:
                str = ''.join(reversed(input[i]))
                ans = str.find(word)
                if ans != -1:
                    start = len(input) - 1 - ans
                    end = start - len(word) + 1

                    res[word] = [(i, start), (i, end)]
                    break

                # If the word is still not found, the while loop moves to the next row.
                else:
                    i += 1
    return res


# This function searches for each word in the list vertically.
def vert_search(input, word_list, res):
    for word in word_list:
        i, j = 0, 0

        # This while loop goes through each column of the search grid and joins the characters together. It then searches
        # the string for the word.
        while j < len(input):
            curr = []
            for i in range(0, len(input)):
                curr.append(input[i][j])

            str = ''.join(curr)
            ans = str.find(word)

            # If the word is found, the word and its coordinates are stored in the dictionary 'res' and the loop ends.
            if ans != -1:
                end = ans + len(word) - 1

                res[word] = [(ans, j), (end, j)]
                break

            # If the word is not found, the column is joined in reverse, and the search for the word is done in the
            # reversed column.
            else:
                str = ''.join(reversed(curr))
                ans = str.find(word)
                if ans != -1:
                    start = len(input) - 1 - ans
                    end = start - len(word) + 1

                    res[word] = [(start, j), (end, j)]
                    break

                # If the word is still not found, the while loop moves to the next column.
                else:
                    j += 1
    return res


# This function searches for each word in the list on the left diagonal (from bottom left to top right).
def left_diag(input, word_list, res):
    for word in word_list:

        # This is a flag to determine if the word has been found.
        found = False

        # 'i' is the number of elements in each diagonal.
        for i in range(0, len(input) - 1):

            # 'curr' is the list of the elements in the current row, and 'locs' is the list of tuples with the row and
            # column for each element.
            curr, locs = [], []

            # 'j' is the element number in each diagonal.
            for j in range(0, i + 1):
                row = i - j

                # The element is appended to curr, and its location is appended to locs.
                curr.append(input[row][j])
                locs.append((row, j))

            str = ''.join(curr)
            ans = str.find(word)

            # If the word is found in the string of the joined list, the tuple with the beginning location of the word
            # is retrieved. The end row and column is calculated based on the length of the word and stored in res.
            if ans != -1:
                beg_loc = locs[ans]
                end_row = beg_loc[0] - len(word) + 1
                end_col = beg_loc[1] + len(word) - 1

                res[word] = [(beg_loc[0], beg_loc[1]), (end_row, end_col)]

                # The found flag is set to true, and the loop ends.
                found = True
                break
            else:

                # If the word is not found, curr is joined in reverse. If the word is found, the tuple with the
                # beginning location of the word is retrieved. The end row and column is calculated based on the length
                # of the word and stored in res.
                str = ''.join(reversed(curr))
                ans = str.find(word)
                if ans != -1:
                    beg_loc = locs[len(str) - ans - 1]
                    end_row = beg_loc[0] + len(word) - 1
                    end_col = beg_loc[1] - len(word) + 1

                    res[word] = [(beg_loc[0], beg_loc[1]), (end_row, end_col)]

                    # The found flag is set to true, and the loop ends.
                    found = True
                    break

        # If the flag is still false indicating the word has not been found, the search continues through the bottom
        # portion of the diagonal.
        if found == False:

            # 'i' starts from the number of elements and decrements.
            for i in range((len(input) - 1), -1, -1):
                curr, locs = [], []

                # 'j' is the element number in each diagonal.
                for j in range(0, i + 1):
                    row = i - j

                    # The element is appended to curr, and its location is appended to locs.
                    curr.append(input[len(input) - j - 1][len(input) - row - 1])
                    locs.append((len(input) - j - 1, len(input) - row - 1))

                    str = ''.join(curr)
                    ans = str.find(word)

                    # If the word is found in the string of the joined list, the tuple with the beginning location of the word
                    # is retrieved. The end row and column is calculated based on the length of the word and stored in res.
                    if ans != -1:
                        beg_loc = locs[ans]
                        end_row = beg_loc[0] - len(word) + 1
                        end_col = beg_loc[1] + len(word) - 1

                        res[word] = [(beg_loc[0], beg_loc[1]), (end_row, end_col)]
                        break

                    # If the word is not found, curr is joined in reverse. If the word is found, the tuple with the
                    # beginning location of the word is retrieved. The end row and column is calculated based on the length
                    # of the word and stored in res.
                    else:
                        str = ''.join(reversed(curr))
                        ans = str.find(word)
                        if ans != -1:
                            beg_loc = locs[len(str) - ans - 1]
                            end_row = beg_loc[0] + len(word) - 1
                            end_col = beg_loc[1] - len(word) + 1

                            res[word] = [(beg_loc[0], beg_loc[1]), (end_row, end_col)]
                            break
    return res


# This function searches for each word in the list on the left diagonal (from bottom right to top left).
def right_diag(input, word_list, res):
    for word in word_list:

        # This is a flag to determine if the word has been found.
        found = False

        # 'i' is the number of elements in each diagonal.
        for i in range(len(input) - 1, -1, -1):
            curr, locs = [], []

            # 'j' is the element number in each diagonal.
            for j in range(0, i + 1):
                row = i - j
                col = len(input) - j - 1

                # The element is appended to curr, and its location is appended to locs.
                curr.append(input[row][col])
                locs.append((row, col))

            str = ''.join(curr)
            ans = str.find(word)

            # If the word is found in the string of the joined list, the tuple with the beginning location of the word
            # is retrieved. The end row and column is calculated based on the length of the word and stored in res.
            if ans != -1:
                beg_loc = locs[ans]
                end_row = beg_loc[0] - len(word) + 1
                end_col = beg_loc[1] - len(word) + 1

                res[word] = [(beg_loc[0], beg_loc[1]), (end_row, end_col)]

                # The found flag is set to true, and the loop ends.
                found = True
                break

            # If the word is not found, curr is joined in reverse. If the word is found, the tuple with the
            # beginning location of the word is retrieved. The end row and column is calculated based on the length
            # of the word and stored in res.
            else:
                str = ''.join(reversed(curr))
                ans = str.find(word)
                if ans != -1:
                    beg_loc = locs[len(str) - ans - 1]
                    end_row = beg_loc[0] + len(word) - 1
                    end_col = beg_loc[1] + len(word) - 1

                    res[word] = [(beg_loc[0], beg_loc[1]), (end_row, end_col)]

                    # This is a flag to determine if the word has been found.
                    found = True
                    break

        if found == False:

            # 'i' starts from the number of elements and decrements.
            for i in range(len(input) - 1, -1, -1):
                curr, locs = [], []

                # 'j' is the element number in each diagonal.
                for j in range(0, i + 1):
                    row = len(input) - j - 1
                    col = i - j

                    # The element is appended to curr, and its location is appended to locs.
                    curr.append(input[row][col])
                    locs.append((row, col))

                    str = ''.join(curr)
                    ans = str.find(word)

                    # If the word is found in the string of the joined list, the tuple with the beginning location of the word
                    # is retrieved. The end row and column is calculated based on the length of the word and stored in res.
                    if ans != -1:
                        beg_loc = locs[ans]
                        end_row = beg_loc[0] - len(word) + 1
                        end_col = beg_loc[1] - len(word) + 1

                        res[word] = [(beg_loc[0], beg_loc[1]), (end_row, end_col)]
                        break

                    # If the word is not found, curr is joined in reverse. If the word is found, the tuple with the
                    # beginning location of the word is retrieved. The end row and column is calculated based on the length
                    # of the word and stored in res.
                    else:
                        str = ''.join(reversed(curr))
                        ans = str.find(word)
                        if ans != -1:
                            beg_loc = locs[len(str) - ans - 1]
                            end_row = beg_loc[0] + len(word) - 1
                            end_col = beg_loc[1] + len(word) - 1

                            res[word] = [(beg_loc[0], beg_loc[1]), (end_row, end_col)]
                            break
    return res

# **** comment below line for testing ****
main()