from src.preprocessing import prepare_data_from_ucimlrepo
from src.model_training import train_and_compare
from src.evaluation import save_all_visualizations
import pandas as pd





def main():
    X, y, preprocessor = prepare_data_from_ucimlrepo()

    df = pd.concat([X, y], axis=1)

    results, X_test_trans, y_test = train_and_compare(X, y, preprocessor, output_dir='models')

    print('\nTrening zakończony. Wyniki:')
    for k,v in results.items():
        print(f'{k}: {v["accuracy"]:.4f}')

    print('\n' + '='*50)
    save_all_visualizations(results, X_test_trans, y_test, df, output_dir='visualizations')
    print('='*50)


if __name__ == '__main__':
    main()