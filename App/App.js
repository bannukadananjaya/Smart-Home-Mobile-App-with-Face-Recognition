import React from 'react';
import { UserProvider } from './Auth/UserContext';
import AppNavigation from './navigation/appNavigation';

export default function App() {
	return (
		<UserProvider>
			<AppNavigation />
		</UserProvider>
	);
}
