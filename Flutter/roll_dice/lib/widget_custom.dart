import 'package:flutter/material.dart';
import 'package:roll_dice/stateful_custom.dart';

class WidgetCustom extends StatelessWidget {
  const WidgetCustom(this.texto, {super.key});
  final String texto;

  @override
  Widget build(context) {
    return Container(
      decoration: BoxDecoration(
          gradient: LinearGradient(colors: [
        const Color.fromARGB(255, 26, 131, 250),
        const Color.fromARGB(255, 74, 158, 254),
      ], begin: Alignment.topCenter, end: Alignment.bottomCenter)),
      // alignment: Alignment.topCenter,
      child: Center(child: StatefulTesteCustom()),
    );
  }
}
