'use strict';

document.addEventListener("DOMContentLoaded", function(event) { 
  updateDelay();
	updateVolume();
});

const updateDelay = () => {
	const delayValue = document.getElementById('delayValue');
	const delay = document.getElementById('delay');
	delayValue.innerHTML = `${delay.value} seconds`;
};

const updateVolume = () => {
	const volumeValue = document.getElementById('volumeValue');
	const volume = document.getElementById('volume');
	volumeValue.innerHTML = `${volume.value}`;
};

const saveForm = () => {
	const wifiName = document.getElementById('wifiName');
	const wifiPassword = document.getElementById('wifiPassword');
	const volume = document.getElementById('volume');
	const delay = document.getElementById('delay');
	const customGoalText = document.getElementById('customGoalText');
	const intermissionTimer = document.getElementById('intermissionTimer');
	const alertOpposingGoal = document.getElementById('alertOpposingGoal');
	
	console.log(wifiName.value);
	console.log(wifiPassword.value);
	console.log(volume.value);
	console.log(delay.value);
	console.log(customGoalText.value);
	console.log(intermissionTimer.value);
	console.log(alertOpposingGoal.value);
}	