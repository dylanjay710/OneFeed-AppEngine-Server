'use strict';

var bitShareApp = bitShareApp || {};
var controllers = bitShareApp.controllers = angular.module('bitShareAppControllers', []);

controllers.controller('RootCtrl', ["$scope", "$location", function ($scope, $location) {

    $scope.onload = function() {
		log("Root Controller laoded");
    }

    $scope.onload();
}]);

controllers.controller('Header1Ctrl', ['$scope', function ($scope) {
	
}]);

controllers.controller('Navbar1Ctrl', ['$scope', function ($scope) {
	
}])

controllers.controller('Body1Ctrl', ['$scope', function ($scope) {
	
}])

controllers.controller('Footer1Ctrl', ['$scope', function ($scope) {
	
}]);
