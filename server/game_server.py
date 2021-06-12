from catan import Catan
import socket
from resource import *
import my_game
from my_constants import *
import audio_server


def tcp_connection_loop(sockets_for_animation, audio_server_socket):
    """
    Add server socket to list
    sockets_for_animation: the list that will contain all Output sockets
    """
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    audio_server_socket = audio_server.Audio_Server()

    try:
        # bind socket to IP and TCP_PORT_NUMBER
        tcp_server_socket.bind((IP, TCP_PORT_NUMBER))

        # become a server socket
        tcp_server_socket.listen(2)
        print("Server for output(animation loop) is listening")
        # connection loop
        j = 0
        while j < NUM_OF_CLIENTS:
            tcp_client_socket, client_address = tcp_server_socket.accept()  # Connected point. Server wait for client
            ip, port = client_address
            print(" Received connection from ip=:", ip, "port=", port)
            sockets_for_animation.append(tcp_client_socket)

            resp = "Wait to start and connect to audio:" + str(j)
            num_str = str(len(resp))
            resp = "".join([num_str.zfill(NUMBER_LENGTH), resp])
            tcp_client_socket.send(resp.encode())

            j = j + 1
    except Exception as e:
        print(e.args)


    finally:
        tcp_server_socket.close()


def receive(server_socket):     # Receives data from the client socket
    try:
        while True:
            data_length = server_socket.recv(NUMBER_LENGTH).decode()
            if data_length is not None and data_length != "":
                data_length = int(data_length)
                data = server_socket.recv(data_length)
                data = data.decode()
                data = data.strip()
                print("message From: " + str(server_socket) + "  " + data)
                return data

    except Exception as e:
        print("3:", e.args)
    return ""


def deal_request(new_game, catan_game, player, request):        # Deals with request from the client
    if type(request) == str and request != "":
        if request.startswith("build_sett:"):
            request = request[11::]
            id, pointId = request.split(":")
            print("Player id:" + id)
            print("Point id:" + pointId)
            player = catan_game.find_player(id)
            point = catan_game.points_object.find_point(pointId)
            response = player.add_sett_point(point, catan_game.points_object)
            new_game.send_to_all_clients(response)

            if player.points == 2:
                earnings = player.sett_points[-1].initial_earning()
                for resource in earnings:
                    player.cards[resource] += earnings[resource]
                res = []
                sum = 0
                for char in earnings:
                    res += [f"{char}{earnings[char]}"]
                    sum += earnings[char]
                response = str(player.id) + "got:" + ",".join(res)
                new_game.send_private_message(player.client_socket, response)
                responseOpp = f"{player.id}got:{sum}"
                for p in catan_game.players:
                    if p.id != player.id:
                        new_game.send_private_message(p.client_socket, responseOpp)

        elif request.startswith("build_road:"):
            request = request[11::]
            id, roadId, pointId = request.split(":")
            player = catan_game.find_player(id)
            road = catan_game.find_road(roadId, pointId)
            player.roads += [road]
            road.canBuild = False
            response = f"build_road:{id}:{roadId}:{pointId}"
            for p in catan_game.players:
                if p.id != player.id:
                    new_game.send_private_message(p.client_socket, response)

        elif request.startswith("dice"):
            num1, num2 = catan_game.dice()
            response = f"dice:{num1}:{num2}"
            new_game.send_to_all_clients(response)
            responses = []
            sum = num1 + num2
            if sum != 7:
                responses = catan_game.getResponse(num1 + num2)
            if responses:
                for response in responses:
                    playerId = response[0]
                    player = catan_game.find_player(playerId)
                    new_game.send_private_message(player.client_socket, response)

        elif request.__contains__("upgrade:"):
            Id_order, pointId = request.split(":")
            playerId = Id_order[0]
            player = catan_game.find_player(playerId)
            point = catan_game.points_object.find_point(pointId)
            player.newCity(point)
            response = request
            for p in catan_game.players:
                if p != player:
                    new_game.send_private_message(p.client_socket, response)
    else:
        request = "Got Nothing From Client"
    return True


def main():
    """
    connection loop
    """
    players = []
    sockets_for_animation = []
    audio_socket = None
    tcp_connection_loop(sockets_for_animation, audio_socket)

    try:

        inputs = sockets_for_animation
        message = ""
        users = {}

        new_game = my_game.Game(sockets_for_animation, message)
        new_game.setDaemon(True)
        new_game.start()
        running = True
        started = False
        available_colors = {"r": "red", "b": "blue", "g": "green"}

        for client_socket in sockets_for_animation:
            request = receive(client_socket)
            print(request)
            if request.__contains__("name:"):
                id, name = request.split(":")
                id = id[0]
                string = "select_color:" + ",".join(list(available_colors.keys()))
                new_game.send_private_message(client_socket, string)
                request = receive(client_socket)
                order, c = request.split(":")
                color = available_colors[c]
                available_colors.__delitem__(c)
                users[name] = [id, color, client_socket]
                # new_game.update(client_socket, request)

        if len(users) == NUM_OF_CLIENTS:
            catan_game = Catan()
            catan_game.set_order(users)
            strings = []
            for player in catan_game.players:
                strings += [player.get_message()]
            string = ",".join(strings)
            final_string = "players" + "[" + string + "]"
            new_game.send_to_all_clients(final_string)

            board_order = catan_game.set_board()
            res = set_resources(board_order)
            order_string = ",".join(board_order)
            new_game.send_to_all_clients("board" + order_string)

            while running:

                if not started:
                    started = True
                    # users = new_game.set_order(users)
                    # new_game.set_board()
                    for player in catan_game.players:
                        start_game(player, new_game, catan_game)

                    print("Starting Reversed Turn")

                    for player in reversed(catan_game.players):
                        start_game(player, new_game, catan_game)

                for player in catan_game.players:
                    mes = f"turn:{player.id}"
                    new_game.send_to_all_clients(mes)
                    while True:
                        request = receive(player.client_socket)
                        if not deal_request(new_game, catan_game, player, request):
                            request = receive(player.client_socket)
                        if request == "finished_turn":
                            break
        # new_game.join(0)    # close new_game thread

    except Exception as e:
        print("2:", e.args)


def start_game(player, new_game, catan_game):       # Starts the game for each player
    mes = f"start_build_sett:{player.id}"
    new_game.send_to_all_clients(mes)
    request = receive(player.client_socket)
    deal_request(new_game, catan_game, player, request)
    response = "start_build_road"
    new_game.send_private_message(player.client_socket, response)
    request = receive(player.client_socket)
    deal_request(new_game, catan_game, player, request)
    request = receive(player.client_socket)
    print("request: " + request)


if __name__ == '__main__':
    main()
