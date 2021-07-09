# messages_1 = ["I am focused", "I am a workaholic", "I like to work"]
# messages_2 = ["I enjoy my life", "I believe in myself", "I am calm"]
fd = open('msgs.txt', 'r')
messages_1 = fd.readlines()
messages_1 = [x.strip() for x in messages_1]
print (messages_1)
messages_2 = messages_1
