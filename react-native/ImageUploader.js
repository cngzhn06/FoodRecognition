import React, { useState } from 'react';
import { View, Button, Image, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

const ImageUploader = () => {
    const [selectedImage, setSelectedImage] = useState(null);

    const pickImage = async () => {
        const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
        const cameraPermissionResult = await ImagePicker.requestCameraPermissionsAsync();

        if (permissionResult.granted === false || cameraPermissionResult.granted === false) {
            Alert.alert("Camera roll ve kamera erişimi gereklidir!");
            return;
        }

        const result = await ImagePicker.launchImageLibraryAsync();
        if (!result.canceled) {
            setSelectedImage(result.assets[0].uri);
        }
    };

    const takePhoto = async () => {
        const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
        const cameraPermissionResult = await ImagePicker.requestCameraPermissionsAsync();

        if (permissionResult.granted === false || cameraPermissionResult.granted === false) {
            Alert.alert("Camera roll ve kamera erişimi gereklidir!");
            return;
        }


        const result = await ImagePicker.launchCameraAsync();

        if (!result.canceled) {
            setSelectedImage(result.assets[0].uri);
        }
    };

    const uploadImage = async () => {
        if (!selectedImage) {
            Alert.alert("Lütfen önce bir görüntü seçin!");
            return;
        }

        const formData = new FormData();
        formData.append('file', {
            uri: selectedImage,
            name: 'photo.jpg',
            type: 'image/jpeg', 
        });


        const response = await fetch('http://127.0.0.1:8000/upload', {
            method: 'POST',
            body: formData,
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        const data = await response.json();
        console.log(data);
        Alert.alert("Sunucudan Gelen Yanıt", JSON.stringify(data));
    };

    return (
        <View style={{ alignItems: 'center', marginTop: 50 }}>
            <Button title="Kütüphaneden Resim Seç" onPress={pickImage} />
            <Button title="Kamera ile Fotoğraf Çek" onPress={takePhoto} />
            {selectedImage && <Image source={{ uri: selectedImage }} style={{ width: 200, height: 200 }} />}
            <Button title="Resmi Yükle" onPress={uploadImage} />
        </View>
    );
};

export default ImageUploader;
