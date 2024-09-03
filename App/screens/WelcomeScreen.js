import { useNavigation } from '@react-navigation/native';
import React from 'react';
import { Image, Text, TouchableOpacity, View } from 'react-native';

export default function WelcomeScreen() {
	const navigation = useNavigation();
	return (
		<View className="flex-1 bg-gray-200">
			<View className="flex justify-around my-4">
				{/* <Text className=" text-white text-center font-bold text-4xl">
					Eco Systems
				</Text> */}
				<View className="flex-row justify-center">
					<Image
						source={require('../assets/images/smart-home.jpg')}
						style={{ width: 500, height: 500 }}
					/>
				</View>

				<View className="space-y-4 mt-0">
					<TouchableOpacity
						onPress={() => navigation.navigate('Login')}
						className="py-3 bg-blue-500 mx-7 rounded-xl"
					>
						<Text className="text-2xl font-bold text-center text-gray-200">
							Log In
						</Text>
					</TouchableOpacity>
					<View className="flex-row justify-center gap-x-2">
						<Text className="text-black font-semibold">
							Don't have an account!
						</Text>
						<TouchableOpacity onPress={() => navigation.navigate('Signup')}>
							<Text className="text-orange-400 font-semibold">Sign Up</Text>
						</TouchableOpacity>
					</View>
				</View>
			</View>
		</View>
	);
}
