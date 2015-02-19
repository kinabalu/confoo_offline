/**
 * Each section of the site has its own module. It probably also has
 * submodules, though this boilerplate is too simple to demonstrate it. Within
 * `src/app/home`, however, could exist several additional folders representing
 * additional modules that would then be listed as dependencies of this one.
 * For example, a `note` section could have the submodules `note.create`,
 * `note.delete`, `note.edit`, etc.
 *
 * Regardless, so long as dependencies are managed correctly, the build process
 * will automatically take take of the rest.
 *
 * The dependencies block here is also where component dependencies should be
 * specified, as shown below.
 */
angular.module( 'ngBoilerplate.home', [
  'ui.router',
  'ngStorage',
  'ui.bootstrap'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider ) {
  $stateProvider
  .state( 'home', {
    url: '/home',
    views: {
      "main": {
        controller: 'HomeCtrl',
        templateUrl: 'home/home.tpl.html'
      }
    },
    /*
    resolve: {
        talks: function(talksService, $stateParams) {
            return talksService.getTalks();
        }
    },*/     
    data:{ pageTitle: 'Home' }
  })
  .state( 'talk', {
    url: '/talk/:talkID',
    views: {
      "main": {
        controller: function ($rootScope, $localStorage, $stateParams, talksService, $scope) {
            $scope.id = $stateParams.talkID;
            $scope.$storage = $localStorage;

            if($rootScope.online) {  
                talksService.getTalk($stateParams.talkID).then(function(talk) {
                    $scope.talk = talk;
                });
            } else {
                filtered_talks = _.filter($scope.$storage.talks, function(element) {
                    return element['id'] === $stateParams.talkID;
                });         

                if(filtered_talks && filtered_talks.length > 0) {
                    $scope.talk = filtered_talks[0];                  
                }
                // $scope.talks = $scope.$storage.talks;
                // $scope.originalTalks = $scope.$storage.talks;
            }

        },
        templateUrl: 'home/talk.tpl.html'
      }
    },
/*    resolve: {
      talk: function(talksService, $stateParams) {
        return talksService.getTalk($stateParams.talkID);
      }
    },
    */
    data:{ pageTitle: 'View Talk' }
  })
  ;
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'HomeCtrl', function HomeController( $rootScope, $scope, $localStorage, talksService, Restangular, talksService ) {
    $scope.$storage = $localStorage;

    $scope.$watch('online', function(newStatus) { 
        console.log("Online:", newStatus);
    });

    if($rootScope.online) {  
        talksService.getTalks().then(function(talks) {
            $scope.talks = _(talks).chain()
              .sortBy('time')
              .sortBy(function(element) {
                  day_of_month = parseInt(element['date'].substr(9, 2));
                  if(day_of_month) {
                    return day_of_month;
                  } else {
                    return 99;
                  }
              })
              .value();
            $scope.originalTalks = Restangular.copy($scope.talks);
            $scope.$storage.talks = $scope.originalTalks;
        });
    } else {
      $scope.talks = $scope.$storage.talks;
      $scope.originalTalks = $scope.$storage.talks;
    }

    $scope.filterDate = function(date) {
        if(date) {
            $scope.talks = _.filter($scope.originalTalks, function(element) {
                return element['date'] == date;
            });          
        } else {
          $scope.talks = $scope.originalTalks;
        }
        $scope.talks = _($scope.talks).chain()
          .sortBy('time')
          .sortBy(function(element) {
              day_of_month = parseInt(element['date'].substr(9, 2));
              if(day_of_month) {
                return day_of_month;
              } else {
                return 99;
              }
          })
          .value();
    };

})

;

