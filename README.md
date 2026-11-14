# Smart Building Security – Komunikacja MQTT

Komunikacja między modułem bezpieczeństwa a panelem internetowym odbywa się przez MQTT z wykorzystaniem brokera Mosquitto.

- **Port:** `1883`
- **Format wiadomości:** JSON
- **Broker:** wspólny dla obu modułów

## 1. Tematy MQTT

| Temat | Kierunek | Opis |
|---|---|---|
| `building/sensors` | Security → Dashboard | Odczyty czujników |
| `building/alerts` | Security → Dashboard | Informacje o alarmach |
| `building/status` | Security → Dashboard | Aktualny stan systemu |
| `building/responses` | Security → Dashboard | Potwierdzenia poleceń |
| `building/commands/alarm` | Dashboard → Security | Sterowanie alarmami |
| `building/commands/mode` | Dashboard → Security | Zmiana trybu pracy |
| `building/commands/sensor` | Dashboard → Security | Włączanie i wyłączanie czujników |

## 2. Wiadomości wysyłane przez Security Module

### Odczyty czujników

Temat: `building/sensors`

```json
{
  "temp_01": 22.5,
  "motion_01": false,
  "door_01": false,
  "window_01": true,
  "smoke_01": false,
  "water_01": false
}
```

Wartości czujników:
- Temperatura – liczba w °C.
- Pozostałe czujniki – `true` / `false`.
- Wyłączony czujnik – `null`.

### Alarmy

Temat: `building/alerts`

```json
{
  "alarm_id": "alarm_001",
  "sensor_id": "smoke_01",
  "type": "fire",
  "severity": "critical",
  "status": "active"
}
```

Planowane wartości `status`: `active`, `reset`.

### Aktualny stan systemu

Temat: `building/status`

```json
{
  "mode": "home",
  "armed": false,
  "active_alarms": [],
  "blocked_sensors": [],
  "disabled_sensors": []
}
```

### Potwierdzenia poleceń

Temat: `building/responses`

Po wykonaniu polecenia system wysyła potwierdzenie jego realizacji oraz aktualny stan systemu.

```json
{
  "command_id": "cmd_001",
  "success": true,
  "mode": "home",
  "armed": false,
  "active_alarms": [],
  "blocked_sensors": [],
  "disabled_sensors": []
}
```

- `command_id` – identyfikator otrzymanego polecenia.
- `success` – informacja, czy polecenie zostało wykonane poprawnie.
- Pozostałe pola – aktualny stan systemu po wykonaniu polecenia.

## 3. Wiadomości odbierane przez Security Module

### Sterowanie alarmami

Temat: `building/commands/alarm`

| Polecenie | Działanie | Dodatkowe pole |
|---|---|---|
| `arm` | Uzbrojenie systemu | – |
| `disarm` | Rozbrojenie systemu | – |
| `reset_all` | Reset wszystkich alarmów | – |
| `reset_one` | Reset pojedynczego alarmu | `alarm_id` |
| `block_sensor` | Blokada alarmowania przez czujnik | `sensor_id` |
| `unblock_sensor` | Odblokowanie alarmowania | `sensor_id` |

Przykłady:

```json
{
  "command": "arm"
}
```

```json
{
  "command": "reset_one",
  "alarm_id": "alarm_001"
}
```

```json
{
  "command": "block_sensor",
  "sensor_id": "motion_01"
}
```

Dla `block_sensor` i `unblock_sensor` można użyć `"sensor_id": "all"` w celu objęcia wszystkich czujników.

### Zmiana trybu pracy

Temat: `building/commands/mode`

```json
{
  "mode": "night"
}
```

Dostępne tryby:

| Tryb | Opis |
|---|---|
| `home` | Domowy |
| `night` | Nocny |
| `away` | Nieobecności |

Tryb pracy i uzbrojenie systemu są niezależnymi ustawieniami.

### Sterowanie czujnikami

Temat: `building/commands/sensor`

| Polecenie | Działanie |
|---|---|
| `enable` | Włączenie czujnika |
| `disable` | Wyłączenie czujnika |

Przykłady:

```json
{
  "command": "disable",
  "sensor_id": "motion_01"
}
```

```json
{
  "command": "enable",
  "sensor_id": "all"
}
```

**Różnica między
