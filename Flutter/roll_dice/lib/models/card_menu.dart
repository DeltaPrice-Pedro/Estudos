import 'package:flutter/material.dart';

class Card extends StatelessWidget {
  const Card(this.titulo, this.preco, this.medida, this.imagem, {super.key});

  final String titulo;
  final String preco;
  final String medida;
  final String imagem;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 100,
      child: Column(
        children: [
          Text(titulo),
          ElevatedButton(onPressed: () {}, child: const Text('Comprar'))
        ],
      ),
    );
  }
}
