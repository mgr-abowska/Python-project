from model import CommentModel
def main():
    model_2 = CommentModel()
    model_2.load()
    print(model_2.predict(['hi', 'max❤️']))

main()

