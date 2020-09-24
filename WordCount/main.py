from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def task():
    try:
        inputfile = "/datafiles/" + request.form['inputfile']
        output = ""
        words = dict()
        
        with open(inputfile) as f:
            for line in f:
                line = line.strip()
                line = line.replace("\n", "")
                for word in line.split(" "):
                    word = word.lower().strip()
                    word = word.replace(" ", "")
                    word = word.replace("\n", "")
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1
            
        for key, value in words.items():
            output = output + key + " " + str(value) + "\n"
            
        output = output.strip()

        return output
    except Exception as e:
        print(e)
        return "- 0"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)