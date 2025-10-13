from src.preprocessing import prepare_data_from_ucimlrepo
from src.model_training import train_and_compare





def main():
    X, y, preprocessor = prepare_data_from_ucimlrepo()
    results = train_and_compare(X, y, preprocessor, output_dir='models')

    print('Trening zakończony. Wyniki:')
    for k,v in results.items():
        print(k, v['accuracy'])


if __name__ == '__main__':
    main()