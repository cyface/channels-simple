var gameControllers = angular.module('gameControllers', ['SwampDragonServices']);

gameControllers.controller('GameController', ['$scope', '$dragon', 'djsession', 'filterFilter', function ($scope, $dragon, djsession, filterFilter) {
    $scope.channel = 'game';
    $scope.game = [];
    $scope.game_pk = -1;
    $scope.player_pk = -1;
    $scope.submitted = false;
    $scope.judging = false;
    $scope.judge_player_pk = -1;
    $scope.all_players_in = false;
    $scope.chosen = false;

    //Called when the swapdragon channels are ready and the socket is open
    $dragon.onReady(function () {
        $scope.game_pk = Number(djsession.game_pk);
        $scope.player_pk = Number(djsession.player_pk);
        $dragon.subscribe('game-route', $scope.channel, {}).then(function (response) {
            this.dataMapper = new DataMapper(response.data);
        });
        $dragon.getSingle('game-route', {'pk': $scope.game_pk}).then(function (response) {
            $scope.game = response.data;
            $scope.updateStatusFields();
        });
    });

    //Update the data when a push is received from the server
    $dragon.onChannelMessage(function (channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function () {
                this.dataMapper.mapData($scope.game, message);
                $scope.updateStatusFields();
            });
        }
    });

    //Called when a player submits a card to the judge
    $scope.submitCard = function (cardgameplayer) {
        if (!$scope.submitted) {
            cardgameplayer.status = 'submitted';
            $scope.submitted = true;
            $dragon.update('cardgameplayer-route', cardgameplayer).catch(function (errors) {
                console.log(errors);
            });
        }
    };

    //Called when a card is chosen as the winner
    $scope.chooseCard = function (cardgameplayer) {
        if ($scope.matching) {
            cardgameplayer.status = 'picked';
            $scope.chosen = true;
            $scope.matching = false;
            submitted_cards = $scope.getCurrentSubmittedCards();
            for (i = 0; i < submitted_cards.length; i++) {
                submitted_cards[i].status = 'lost';
            }

            //Also need to draw new card for hands, and new matching card
            $dragon.update('cardgameplayer-route', cardgameplayer).catch(function (errors) {
                console.log(errors);
            });
        }
    };

    $scope.getCurrentSubmittedCards = function () {
        return filterFilter($scope.game.cardgameplayer_set, {status: 'submitted'})
    };

    //Update the status fields in the current session to match the data
    $scope.updateStatusFields = function () {
        if ($scope.game.players) {
            var this_player_submitted = filterFilter($scope.game.cardgameplayer_set, {status: 'submitted', player: {id: $scope.player_pk}});
            $scope.submitted = this_player_submitted.length > 0;

            var this_player_matching = filterFilter($scope.game.cardgameplayer_set, {status: 'matching', player: {id: $scope.player_pk}});
            $scope.matching = this_player_matching.length > 0;

            var matching_card_list = filterFilter($scope.game.cardgameplayer_set, {status: 'matching'});
            if (matching_card_list.length == 1) {
                $scope.judge_player_pk = Number(matching_card_list[0].player.id);
            }

            var player_count = $scope.game.players.length;
            var submitted_cards = $scope.getCurrentSubmittedCards();
            $scope.all_players_in = player_count > 1 && player_count - 1 <= submitted_cards.length;

        }
    }

}]);
