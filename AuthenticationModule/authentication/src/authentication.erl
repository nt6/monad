%% Copyright 2015 Ericsson AB
%%
%% Licensed under the Apache License, Version 2.0 (the "License"); you may not
%% use this file except in compliance with the License. You may obtain a copy
%% of the License at
%%
%%    http://www.apache.org/licenses/LICENSE-2.0
%%
%% Unless required by applicable law or agreed to in writing, software
%% distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
%% WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
%% License for the specific language governing permissions and limitations
%% under the License.

%% @doc The following file is based on MochiWeb (Available at: https://github.com/mochi/mochiweb)
%%      @author Mochi Media <dev@mochimedia.com>
%%      @copyright 2010 Mochi Media <dev@mochimedia.com>

-module(authentication).

-export([start/0, stop/0]).

ensure_started(App) ->
    case application:start(App) of
        ok ->
            ok;
        {error, {already_started, App}} ->
            ok
    end.


%% @spec start() -> ok
%% @doc Start the authentication server.
start() ->
    authentication_deps:ensure(),
    ensure_started(crypto),
    application:start(authentication).


%% @spec stop() -> ok
%% @doc Stop the authentication server.
stop() ->
    application:stop(authentication).
