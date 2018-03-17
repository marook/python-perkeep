#
# Copyright 2018 Markus Peröbner
#
import perkeep

def main():
    query_solln()

def query_solln():
    results = perkeep.query({
        'expression': 'tag:solln',
        'describe': {
            'depth': 1,
            'rules': [
                {
                    'attrs': [
                        'camliContent',
                    ],
                },
            ],
        },
    })
    for blob in results['blobs']:
        description = results['description']['meta'][blob['blob']]
        if(not 'title' in description['permanode']['attr']):
            continue
        print(description['permanode']['attr']['title'][0])

if __name__ == '__main__':
    main()
