import { useNavigation } from '@react-navigation/native';
import React from 'react';
import { Text, TouchableOpacity, View } from 'react-native';

export default function HomeScreen() {
	const navigation = useNavigation();
	return (
		<View className="flex-1 justify-center bg-blue-500 pt-8">
			<Text className="text-4xl font-bold text-white text-center m-16">
				Smart Home App
			</Text>
			<View
				className="flex-1 bg-white px-8 pt-8"
				style={{ borderTopLeftRadius: 50, borderTopRightRadius: 50 }}
			>
				<TouchableOpacity
					onPress={() => navigation.navigate('FaceRecognition')}
					className="rounded-xl bg-slate-700 p-4 m-4 shadow-lg"
				>
					<Text className="text-2xl text-center text-cyan-100 font-bold">
						Face Recognition
					</Text>
				</TouchableOpacity>
				<TouchableOpacity
					onPress={() => navigation.navigate('Log Details')}
					className="rounded-xl bg-slate-700 p-4 m-4 shadow-lg"
				>
					<Text className="text-2xl text-center text-cyan-100 font-bold">
						Log Details
					</Text>
				</TouchableOpacity>
				<TouchableOpacity
					onPress={() => navigation.navigate('People')}
					className="rounded-xl bg-slate-700 p-4 m-4  shadow-lg"
				>
					<Text className="text-2xl text-center text-cyan-100 font-bold">
						People
					</Text>
				</TouchableOpacity>
			</View>
		</View>
	);
}
