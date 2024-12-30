import 'package:flutter/material.dart';
import 'dart:math';

class StatefulTeste extends StatefulWidget {
  const StatefulTeste({super.key});

  @override
  State<StatefulTeste> createState() {
    return _StatefulTeste();
  }
}

class _StatefulTeste extends State<StatefulTeste> {
  String textChange = 'Sesas Num.: Null';
  var random = Random();

  void method() {
    int randomNum = random.nextInt(11);
    setState(() {
      textChange = 'Sesas Num.: $randomNum';
    });
  }

  @override
  Widget build(context) {
    return Column(children: [
      Opacity(
        opacity: 0.2,
        child: Image.asset(
          'assets/images/deltaprice_hori.png',
          width: 400,
        ),
      ),
      Text(
        textChange,
        style: TextStyle(fontSize: 40),
      ),
      TextButton.icon(
          onPressed: method,
          style: TextButton.styleFrom(
              padding: const EdgeInsets.only(top: 20),
              minimumSize: Size(40, 40)),
          icon: const Icon(Icons.import_contacts_sharp),
          label: const Text('Enviar')),
    ]);
  }
}
