// App.js

import React from 'react';
import { SafeAreaView } from 'react-native';
import ImageUploader from './ImageUploader';

const App = () => {
    return (
        <SafeAreaView style={{ flex: 1 }}>
            <ImageUploader />
        </SafeAreaView>
    );
};

export default App;
