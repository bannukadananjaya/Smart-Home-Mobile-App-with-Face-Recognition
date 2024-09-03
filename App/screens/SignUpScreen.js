import { useNavigation } from '@react-navigation/native';
import axios from 'axios';
import React, { useState } from 'react';
import { Alert, Text, TextInput, TouchableOpacity, View } from 'react-native';
// import api from '../route/baseURL';

export default function SignUpScreen() {
	const navigation = useNavigation();

	const [userName, setUserName] = useState('');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');

	const handleSignup = async () => {
		try {
			const response = await axios.post('http://192.168.8.100:8000/signup/', {
				username: userName,
				email: email,
				password: password,
			});

			if (response.status === 200) {
				navigation.navigate('Login');
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
			<Text className="text-6xl font-bold mb-4 text-center mt-16 m-16">
				Sign Up
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
					<Text className="text-gray-700 ml-4">Email Address:</Text>
					<TextInput
						placeholder="Email Address"
						className="border-gray-400 bg-gray-100 text-gray-700 border mb-3 p-2 rounded-2xl"
						value={email}
						onChangeText={setEmail}
					/>
					<Text className="text-gray-700 ml-4">Password:</Text>
					<TextInput
						placeholder="Password"
						secureTextEntry
						className="border-gray-400 bg-gray-100 text-gray-700 border mb-3 p-2 rounded-2xl"
						value={password}
						onChangeText={setPassword}
					/>
					<Text className="text-gray-700 ml-4">Confirm Password:</Text>
					<TextInput
						placeholder="Password"
						secureTextEntry
						className="border-gray-400 bg-gray-100 text-gray-700 border mb-3 p-2 rounded-2xl"
						value={confirmPassword}
						onChangeText={setConfirmPassword}
					/>
					<TouchableOpacity
						className="bg-blue-500 p-2 rounded"
						onPress={handleSignup}
					>
						<Text className="font-xl font-bold text-white text-center">
							Sign Up
						</Text>
					</TouchableOpacity>
				</View>
			</View>
		</View>
	);
}
