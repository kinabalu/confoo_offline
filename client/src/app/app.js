angular.module( 'ngBoilerplate', [
  'restangular',
  'templates-app',
  'templates-common',
  'ngBoilerplate.home',
  'ngBoilerplate.about',
  'ui.router'
])

.config( function myAppConfig ( $stateProvider, $urlRouterProvider, RestangularProvider ) {
  $urlRouterProvider.otherwise( '/home' );
  RestangularProvider.setBaseUrl('http://confoo.mystic5.com/api');
  // RestangularProvider.setBaseUrl('http://localhost:8080/api');

  RestangularProvider.addResponseInterceptor(function (data, operation, what, url, response, deferred) {  

    // console.log(data);
    switch(operation) {
      case 'getList':
        // console.log("getList");
        return data.objects;
      default:
        return data;
    }
  });

})

.run( function run ($window, $rootScope) {

      $rootScope.online = navigator.onLine;
      $window.addEventListener("offline", function () {
        $rootScope.$apply(function() {
          $rootScope.online = false;
        });
      }, false);
      $window.addEventListener("online", function () {
        $rootScope.$apply(function() {
          $rootScope.online = true;
        });
      }, false);  
})

.factory("talksService", function(Restangular){
    return {
        getTalks: function(filter){
            if(filter) {
                return Restangular.all("talks").getList({filterBy: filter}).$object;
            } else {
                return Restangular.all("talks").getList();
            }
        },
        removeTalk: function(selectedTalk, talks) {
            var index = talks.indexOf(selectedTalk);
            if(index > -1) {
                talks.splice(index, 1);
            }
        },
        getTalk: function(id) {
            return Restangular.one("talks", id).get();
        },
        updateTalk: function(talk) {
            return talk.put();
        },
        addTalk: function(talk) {
            return Restangular.all("talks")
                .post(talk);
        }
    };
})

.controller( 'AppCtrl', function AppCtrl ( $scope, $location ) {
  $scope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams){
    if ( angular.isDefined( toState.data.pageTitle ) ) {
      $scope.pageTitle = toState.data.pageTitle + ' | ngBoilerplate' ;
    }
  });
})

;

