import axios from 'axios';
import React, { useEffect, useState } from 'react';
import {
	Text,
	View,
	FlatList,
	TouchableOpacity,
	TextInput,
	Alert,
} from 'react-native';

export default function LogDetailsScreen() {
	const [logs, setLogs] = useState([]);
	const [date, setDate] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const fetchLogs = async () => {
		try {
			setIsLoading(true);
			const response = await axios.get(
				'https://e0fe-192-248-58-1.ngrok-free.app/logs',
				{
					params: { date },
				}
			);
			setLogs(response.data);
		} catch (error) {
			console.error(error);
			Alert.alert('Error', 'Failed to fetch logs.');
		} finally {
			setIsLoading(false);
		}
	};

	useEffect(() => {
		if (date) fetchLogs();
	}, [date]);

	return (
		<View className="flex-1 justify-center bg-blue-500">
			<Text className="text-4xl font-bold text-white text-center my-4">
				Log Details
			</Text>
			<View
				className="bg-white p-4 rounded-t-3xl"
				style={{ flex: 1, borderTopLeftRadius: 50, borderTopRightRadius: 50 }}
			>
				<TextInput
					placeholder="Enter date (YYYY-MM-DD)"
					value={date}
					onChangeText={setDate}
					className="bg-gray-200 p-2 rounded-lg mb-4"
				/>
				{isLoading ? (
					<Text className="text-center text-lg">Loading...</Text>
				) : (
					<FlatList
						data={logs}
						keyExtractor={(item) => item.id.toString()}
						renderItem={({ item }) => (
							<View className="p-2 border-b border-gray-300">
								<Text className="text-lg">User: {item.username}</Text>
								<Text className="text-lg">Entry Time: {item.entry_time}</Text>
							</View>
						)}
					/>
				)}
			</View>
		</View>
	);
}
