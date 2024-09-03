import { useNavigation } from '@react-navigation/native';
import axios from 'axios';
import React, { useState } from 'react';
import { Alert, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { useUser } from '../Auth/UserContext';
// import api from '../route/baseURL';

export default function LoginScreen() {
	const navigation = useNavigation();

	const [userName, setUserName] = useState('');
	const [password, setPassword] = useState('');
	const { setUser } = useUser();

	const handleLogin = async () => {
		console.log(userName);
		console.log(password);

		try {
			const response = await axios.post('http://192.168.1.5:8000/login', {
				username: userName,
				password: password,
			});

			if (response.status === 200) {
				console.log('OK');
				console.log(response.data);
				setUser(response.data.user_id);
				navigation.navigate('Home');
			} else {
				Alert.alert('Login Failed', 'Invalid credentials');
			}
		} catch (error) {
			Alert.alert('Error', 'Something went wrong. Please try again.');
			console.log(error);
		}
	};

	return (
		<View className="flex-1 justify-center pt-8 bg-blue-500">
			<Text className="text-6xl text-white font-bold mb-4 text-center mt-16 m-16">
				Login
			</Text>
			<View
				className="flex-1 bg-white px-8 pt-8"
				style={{ borderTopLeftRadius: 50, borderTopRightRadius: 50 }}
			>
				<View className="form space-y-2">
					<Text className="text-gray-700 ml-4">User Name:</Text>
					<TextInput
						placeholder="Username"
						className="border-gray-400 bg-gray-100 text-gray-700 border mb-3 p-2 rounded-2xl"
						value={userName}
						onChangeText={setUserName}
					/>
					<Text className="text-gray-700 ml-4">Password:</Text>
					<TextInput
						placeholder="Password"
						secureTextEntry
						className="border-gray-400 bg-gray-100 text-gray-700 border mb-3 p-2 rounded-2xl"
						value={password}
						onChangeText={setPassword}
					/>
					<TouchableOpacity
						className="bg-blue-500 p-2 rounded "
						onPress={handleLogin}
					>
						<Text className="text-2xl font-bold text-center text-gray-200">
							Login
						</Text>
					</TouchableOpacity>
				</View>
			</View>
		</View>
	);
}
