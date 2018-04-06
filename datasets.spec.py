from perkeep import datasets

def main():
    ds = datasets.build_from_resource_identifier('pk:attr:"per:type":dataset')

    pl = datasets.Pipeline()
    pl.reducers.append([
        'tread_right_velocity',
        'tread_left_velocity',
        'word',
        'random',
    ])
    pl.extenders.append(build_extender('e1'))
    pl.extenders.append(build_extender('e2'))
    pl.x_mapper = lambda s: (s['name'], s['i'], s['tread_right_velocity'], s['tread_left_velocity'], s['word'])
    pl.y_mapper = lambda s: (s['random'])
    pl.batch_size = 2

    all_samples = pl.get(ds.samples)
    print('total: {}'.format(len(all_samples)))
    print_some(all_samples)
    splitted_samples = pl.split(ds.samples)
    for c in pl.categories.keys():
        samples = splitted_samples[c]
        print('{} samples: {}'.format(c, len(samples)))
        print_some(samples)
    print('train batch arrays')
    print_some(splitted_samples['train'].batch_arrays())

def build_extender(name):
    def extender(sample):
        for i in range(2):
            def mapper(key, sample):
                val = sample[key]
                if(key == 'random' and not val is None):
                    return 10*val
                else:
                    return val

            sample = datasets.MappingSample(sample, mapper)
            sample = datasets.MixinSample(sample, {
                'name': name,
                'i': i,
            })
            yield sample
    return extender

def print_some(items):
    for i, item in enumerate(items):
        if(i >= 5):
            break
        print('  [{}] {}'.format(i, item))

if __name__ == '__main__':
    main()
