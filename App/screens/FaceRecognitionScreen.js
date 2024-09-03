// import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Alert, Text, TouchableOpacity, View } from 'react-native';
import { useUser } from '../Auth/UserContext';
import api from '../route/baseURL';

export default function FaceRecognitionScreen() {
	const { user } = useUser();
	const [isLoading, setIsLoading] = useState(false);

	const captureImage = async () => {
		try {
			setIsLoading(true);
			const response = await api.post(
				`capture_images/${user}`
			);
			Alert.alert(
				'Success',
				response.data.message || 'Image captured successfully.'
			);
		} catch (error) {
			console.error(error);
			Alert.alert('Error', 'Failed to capture images.');
		} finally {
			setIsLoading(false);
		}
	};

	const trainModel = async () => {
		try {
			setIsLoading(true);
			const response = await api.post(
				'train_model'
			);
			Alert.alert(
				'Success',
				response.data.message || 'Model trained successfully.'
			);
		} catch (error) {
			console.error(error);
			Alert.alert('Error', 'Failed to train the model.');
		} finally {
			setIsLoading(false);
		}
	};

	const recognizePerson = async () => {
		try {
			setIsLoading(true);

			// Step 1: Recognize the person
			const response = await api.post(
				'recognize_person'
			);
			console.log(response.data.message);
			Alert.alert(
				'Success',
				response.data.message || 'Person recognized successfully.'
			);

			// Step 2: Log the entry
			const now = new Date();
			const entryTime = now.toISOString().split('.')[0]; // "2024-08-27T15:00:00"
			const date = now.toISOString().split('T')[0]; // "2024-08-27"

			try {
				await api.post('logs', {
					user_id: user,
					entry_time: entryTime,
					date: date,
				});

				console.log('Entry recorded successfully.');
				Alert.alert('Success', 'Entry recorded successfully.');
			} catch (error) {
				console.error(error);
				Alert.alert('Error', 'Failed to record entry.');
			}

			// Step 3: Call the door handle API to blink the LED
			try {
				const doorHandleResponse = await api.get(
					'doorHandle/'
				);
				console.log(doorHandleResponse.data.message);
				Alert.alert(
					'Success',
					doorHandleResponse.data.message || 'Door unlocked successfully.'
				);
			} catch (error) {
				console.error('Error unlocking the door:', error);
				Alert.alert('Error', 'Failed to unlock the door.');
			}
		} catch (error) {
			console.error(error);
			Alert.alert('Error', 'Failed to recognize person.');
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<View className="flex-1 justify-center bg-blue-500">
			<Text className="text-6xl font-bold text-white text-center m-16">
				Door Handle
			</Text>
			<View
				className="flex-1 bg-white px-8 pt-8"
				style={{ borderTopLeftRadius: 50, borderTopRightRadius: 50 }}
			>
				<TouchableOpacity
					onPress={captureImage} // Invoke function
					className="rounded-xl bg-slate-700 p-4 m-4 shadow-lg"
					disabled={isLoading || !user} // Disable if loading or personId is not set
				>
					<Text className="text-2xl text-center text-cyan-100 font-bold">
						Face Register
					</Text>
				</TouchableOpacity>
				<TouchableOpacity
					onPress={trainModel} // Invoke function
					className="rounded-xl bg-slate-700 p-4 m-4 shadow-lg"
					disabled={isLoading} // Disable if loading
				>
					<Text className="text-2xl text-center text-cyan-100 font-bold">
						Face Train
					</Text>
				</TouchableOpacity>
				<TouchableOpacity
					onPress={recognizePerson} // Invoke function
					className="rounded-xl bg-slate-700 p-4 m-4 shadow-lg"
					disabled={isLoading} // Disable if loading
				>
					<Text className="text-2xl text-center text-cyan-100 font-bold">
						Face Recognition
					</Text>
				</TouchableOpacity>
			</View>
		</View>
	);
}
