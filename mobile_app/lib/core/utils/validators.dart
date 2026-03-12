class Validators {
  static bool isEmail(String input) {
    final value = input.trim();
    return RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(value);
  }

  static bool minLength(String input, int len) => input.trim().length >= len;
}
