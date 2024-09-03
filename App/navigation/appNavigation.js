import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import React from 'react';

import FaceRecognitionScreen from '../screens/FaceRecognitionScreen';
import HomeScreen from '../screens/HomeScreen';
import LoginScreen from '../screens/LoginScreen';
import SignUpScreen from '../screens/SignUpScreen';
import WelcomeScreen from '../screens/WelcomeScreen';

export default function appNavigation() {
	const Stack = createNativeStackNavigator();

	return (
		<NavigationContainer>
			<Stack.Navigator initialRouteName="Welcome">
				<Stack.Screen
					name="Home"
					options={{ headerShown: false }}
					component={HomeScreen}
				/>
				<Stack.Screen
					name="Welcome"
					options={{ headerShown: false }}
					component={WelcomeScreen}
				/>
				<Stack.Screen
					name="Login"
					options={{ headerShown: false }}
					component={LoginScreen}
				/>
				<Stack.Screen
					name="Signup"
					options={{ headerShown: false }}
					component={SignUpScreen}
				/>
				<Stack.Screen
					name="FaceRecognition"
					options={{ headerShown: false }}
					component={FaceRecognitionScreen}
				/>
			</Stack.Navigator>
		</NavigationContainer>
	);
}
