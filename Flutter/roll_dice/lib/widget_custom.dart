import 'package:flutter/material.dart';

class WidgetCustom extends StatelessWidget {
  const WidgetCustom(this.texto, {super.key});
  final String texto;

  @override
  Widget build(context) {
    return Container(
      decoration: BoxDecoration(
          gradient: LinearGradient(colors: [
        const Color.fromARGB(255, 3, 115, 244),
        const Color.fromARGB(255, 182, 215, 253),
      ], begin: Alignment.topLeft, end: Alignment.bottomRight)),
      // alignment: Alignment.topCenter,
      child: Center(
          child: Image.asset(
        'assets/images/deltaprice_hori.png',
        width: 400,
      )),
    );
  }
}
