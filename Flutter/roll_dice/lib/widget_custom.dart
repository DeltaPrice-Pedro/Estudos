import 'package:flutter/material.dart';

class WidgetCustom extends StatelessWidget {
  const WidgetCustom(this.texto, {super.key});
  final String texto;

  void method() {}

  @override
  Widget build(context) {
    return Container(
      decoration: BoxDecoration(
          gradient: LinearGradient(colors: [
        const Color.fromARGB(255, 10, 103, 210),
        const Color.fromARGB(255, 3, 115, 244),
        const Color.fromARGB(255, 182, 215, 253),
      ], begin: Alignment.topCenter, end: Alignment.bottomCenter)),
      // alignment: Alignment.topCenter,
      child: Center(
          child: Column(children: [
        Image.asset(
          'assets/images/deltaprice_hori.png',
          width: 400,
        ),
        TextButton(
            onPressed: method,
            style:
                TextButton.styleFrom(padding: const EdgeInsets.only(top: 20)),
            child: const Text('Enviar')),
      ])),
    );
  }
}
