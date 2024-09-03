import { View, Text, TouchableOpacity } from 'react-native';
import React from 'react';
import { useNavigation } from '@react-navigation/native';

export default function DeviceControl() {
	const navigation = useNavigation();

	return (
		<View className="flex-1 justify-center p-4">
			<Text className="text-2xl font-bold mb-4">Device Control</Text>
			<TouchableOpacity
				className="bg-blue-500 p-3 rounded"
				onPress={() => navigation.navigate('FaceRecognition')}
			>
				<Text className="text-white text-center">Go to Face Recognition</Text>
			</TouchableOpacity>
		</View>
	);
}
