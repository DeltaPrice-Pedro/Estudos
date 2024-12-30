import 'package:flutter/material.dart';
import 'dart:math';

class StatefulTesteCustom extends StatefulWidget {
  const StatefulTesteCustom({super.key});

  @override
  State<StatefulTesteCustom> createState() {
    return _StatefulTesteCustom();
  }
}

class _StatefulTesteCustom extends State<StatefulTesteCustom> {
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
      Image.asset(
        'assets/images/deltaprice_hori.png',
        width: 400,
      ),
      Text(
        textChange,
        style: TextStyle(fontSize: 40),
      ),
      TextButton(
          onPressed: method,
          style: TextButton.styleFrom(
              padding: const EdgeInsets.only(top: 20),
              minimumSize: Size(40, 40)),
          child: const Text('Enviar')),
    ]);
  }
}
